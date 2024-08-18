import threading
import time
import json
import board
import busio
from gpiozero import Motor, PWMOutputDevice
from adafruit_servokit import ServoKit
import paho.mqtt.client as mqtt

# I2C 버스 설정 (SCL 및 SDA 핀을 사용하여 I2C 버스 초기화)
SCL_PIN = board.D1  # GPIO 1
SDA_PIN = board.D0  # GPIO 0
i2c_bus = busio.I2C(SCL_PIN, SDA_PIN)

def i2c_scan(i2c):
    """
    I2C 버스를 스캔하여 연결된 모든 I2C 장치의 주소를 반환합니다.
    """
    while not i2c.try_lock():
        pass
    try:
        devices = i2c.scan()
        return devices
    finally:
        i2c.unlock()

def initialize_servo():
    try:
        print("Scanning I2C bus...")
        # I2C 버스를 스캔하여 연결된 장치 목록을 가져옴
        devices = i2c_scan(i2c_bus)
        print(f"I2C devices found: {[hex(device) for device in devices]}")

        if not devices:
            raise ValueError("No I2C devices found on the bus.")

        # PCA9685 PWM 드라이버 초기화 (서보 모터 제어를 위해 사용)
        kit = ServoKit(channels=16, i2c=i2c_bus, address=0x60)
        print("PCA9685 initialized at address 0x60.")

        return kit
    except Exception as e:
        print(f"Error initializing PCA9685: {e}")
        raise

# 방향 매핑
directions_mapping = {
    (-1, 0): 'N',  # 북쪽
    (1, 0): 'S',   # 남쪽
    (0, -1): 'W',  # 서쪽
    (0, 1): 'E',   # 동쪽
    (-1, -1): 'H', # 북서쪽
    (-1, 1): 'J',  # 북동쪽
    (1, -1): 'Z',  # 남서쪽
    (1, 1): 'X'    # 남동쪽
}

# 서보 각도 매핑
direction_angles = {
    'C': 120,       # 중앙
    'L': 60,        # 좌회전
    'R': 180,       # 우회전
    'LD': 90,       # 좌대각선
    'RD': 150       # 우대각선
}

# 모터 상태
STOP = 0
FORWARD = 1
BACKWARD = 2

# 실제 핀 정의
# PWM PIN
ENA = 26  # GPIO 26(37 pin)

# GPIO PIN
IN1 = 19  # GPIO 19(37 pin)
IN2 = 13  # GPIO 13(35 pin)

# 모터 핀 설정
motor1 = Motor(forward=IN1, backward=IN2)

# PWM 설정
pwmA = PWMOutputDevice(ENA)

# 모터 제어 함수
def setMotor(motor, pwm, speed, stat):
    pwm.value = speed / 100.0
    if stat == FORWARD:
        motor.forward()
    elif stat == BACKWARD:
        motor.backward()
    elif stat == STOP:
        motor.stop()

# 전역 변수로 인덱스 및 장애물 감지 상태 저장
current_direction_index = 0
obstacle_detected = False
obstacle_location = "unknown"
current_direction = ''  # 현재 방향을 추적하기 위한 변수
back_drive = 0

def control_motor(directions, stop_event):
    """
    모터를 제어하여 방향에 따라 전진 및 후진을 수행하는 함수
    :param directions: 방향 리스트
    :param stop_event: 종료 이벤트
    """

    global current_direction_index, obstacle_detected, current_direction

    try:
         # 초기 방향 설정
        for direction in directions:
            if obstacle_detected:
                break

            if stop_event.is_set():
                break

            if current_direction != direction:
                # 방향이 다를 때 속도 줄이기
                print("Slowing down for turn")
                setMotor(motor1, pwmA, 70, FORWARD)  # 방향 전환 전 속도 줄이기
                # 서보와 동기화
                time.sleep(2)  # 서보가 각도로 이동할 시간을 기다리기
            else:
                # 방향이 같을 때 전진 속도 유지
                setMotor(motor1, pwmA, 40, FORWARD)  # 전진 30% 속도
                time.sleep(2)  # 서보와 동기화

            # 현재 방향 업데이트
            current_direction = direction

        print("Reached the end of directions.")
    except KeyboardInterrupt:
        stop_event.set()  # 종료 이벤트 설정
    finally:
        setMotor(motor1, pwmA, 0, STOP)  # 모터 정지
        print("Motor control stopped.")
        stop_event.set()

def control_servo(kit, directions, stop_event):
    """
    서보 모터를 제어하여 방향에 따라 각도를 조절하는 함수
    :param kit: ServoKit 인스턴스
    :param directions: 방향 리스트
    :param stop_event: 종료 이벤트
    """

    global current_direction_index, obstacle_detected, current_direction

    try:
        for direction in directions:
            if obstacle_detected:
                break

            if stop_event.is_set():
                break

            # 현재 방향과 목표 방향이 같으면 서보를 중앙으로 설정
            if current_direction == direction:
                kit.servo[0].angle = direction_angles['C']
                print(f"Current direction is {current_direction}. Servo reset to center (120 degrees).")
                # 모터와 동기화
                time.sleep(2)  # 중앙으로 이동 후 대기
            else:
                # 방향 매핑을 통해 현재 방향과 목표 방향을 결정
                angle = get_servo_angle(current_direction, direction)
                if angle is not None:
                    kit.servo[0].angle = angle
                    print(f"Servo set to {direction} direction ({angle} degrees)")
                    time.sleep(2)  # 서보 위치 유지 시간

            current_direction = direction  # 현재 방향 업데이트

        # 모든 방향이 완료된 후 서보를 중앙으로 복귀
        kit.servo[0].angle = direction_angles['C']
        print("Completed all directions. Servo reset to center (120 degrees).")
    except KeyboardInterrupt:
        stop_event.set()  # 종료 이벤트 설정
    finally:
        kit.servo[0].angle = direction_angles['C']  # 서보 초기 위치
        print("Servo control stopped.")
        stop_event.set()

def get_servo_angle(current_direction, target_direction):
    """
    현재 방향과 목표 방향을 기반으로 서보 각도를 결정하는 함수
    :param current_direction: 현재 방향
    :param target_direction: 목표 방향
    :return: 서보 각도
    """
    global back_drive

    if current_direction == 'N':
        if target_direction == 'W':
            if back_drive == 0:
                return direction_angles['L']
            else:
                return direction_angles['R']
        elif target_direction == 'E':
            if back_drive == 0:
                return direction_angles['R']
            else:
                return direction_angles['L']
        elif target_direction == 'H':
            if back_drive == 0:
                return direction_angles['LD']
            else:
                return direction_angles['RD']
        elif target_direction == 'J':
            if back_drive == 0:
                return direction_angles['RD']
            else:
                return direction_angles['LD']
    elif current_direction == 'S':
        if target_direction == 'E':
            if back_drive == 0:
                return direction_angles['L']
            else:
                return direction_angles['R']
        elif target_direction == 'W':
            if back_drive == 0 :
                return direction_angles['R']
            else:
                return direction_angles['L']
        elif target_direction == 'X':
            if back_drive == 0:
                return direction_angles['LD']
            else :
                return direction_angles['RD']
        elif target_direction == 'Z':
            if back_drive == 0:
                return direction_angles['RD']
            else:
                return direction_angles['LD']
    elif current_direction == 'E':
        if target_direction == 'N':
            if back_drive == 0:
                return direction_angles['L']
            else:
                return direction_angles['R']
        elif target_direction == 'S':
            if back_drive == 0:
                return direction_angles['R']
            else:
                return direction_angles['L']
        elif target_direction == 'J':
            if back_drive == 0:
                return direction_angles['LD']
            else:
                return direction_angles['RD']
        elif target_direction == 'X':
            if back_drive == 0:
                return direction_angles['RD']
            else:
                return direction_angles['LD']
    elif current_direction == 'W':
        if target_direction == 'S':
            if back_drive == 0:
                return direction_angles['L']
            else:
                return direction_angles['R']
        elif target_direction == 'N':
            if back_drive == 0:
                return direction_angles['R']
            else:
                return direction_angles['L']
        elif target_direction == 'H':
            if back_drive == 0:
                return direction_angles['RD']
            else:
                return direction_angles['LD']
        elif target_direction == 'Z':
            if back_drive == 0:
                return direction_angles['LD']
            else:
                return direction_angles['RD']
    elif current_direction == 'H':
        if target_direction == 'N':
            if back_drive == 0:
                return direction_angles['RD']
            else:
                return direction_angles['LD']
        elif target_direction == 'J':
            if back_drive == 0:
                return direction_angles['R']
            else:
                return direction_angles['L']
        elif target_direction == 'W':
            if back_drive == 0:
                return direction_angles['LD']
            else:
                return direction_angles['RD']
        elif target_direction == 'Z':
            if back_drive == 0:
                return direction_angles['L']
            else:
                return direction_angles['R']
    elif current_direction == 'J':
        if target_direction == 'E':
            if back_drive == 0:
                return direction_angles['RD']
            else:
                return direction_angles['LD']
        elif target_direction == 'X':
            if back_drive == 0:
                return direction_angles['R']
            else:
                return direction_angles['L']
        elif target_direction == 'N':
            if back_drive == 0:
                return direction_angles['LD']
            else:
                return direction_angles['RD']
        elif target_direction == 'H':
            if back_drive == 0:
                return direction_angles['L']
            else:
                return direction_angles['R']
    elif current_direction == 'Z':
        if target_direction == 'S':
            if back_drive == 0:
                return direction_angles['LD']
            else:
                return direction_angles['RD']
        elif target_direction == 'H':
            if back_drive == 0:
                return direction_angles['R']
            else:
                return direction_angles['L']
        elif target_direction == 'W':
            if back_drive == 0:
                return direction_angles['RD']
            else:
                return direction_angles['LD']
        elif target_direction == 'X':
            if back_drive == 0:
                return direction_angles['L']
            else:
                return direction_angles['R']
    elif current_direction == 'X':
        if target_direction == 'J':
            if back_drive == 0:
                return direction_angles['L']
            else:
                return direction_angles['R']
        elif target_direction == 'Z':
            if back_drive == 0:
                return direction_angles['R']
            else:
                return direction_angles['L']
        elif target_direction == 'E':
            if back_drive == 0:
                return direction_angles['LD']
            else:
                return direction_angles['RD']
        elif target_direction == 'S':
            if back_drive == 0:
                return direction_angles['RD']
            else:
                return direction_angles['LD']
    return None

def on_connect(client, userdata, flags, rc):
    print("Connected!")
    client.subscribe("ultrasonic/detect/object")

def on_message(client, userdata, msg):
    """
    MQTT 메시지 수신 시 호출되는 콜백 함수
    :param client: MQTT 클라이언트 인스턴스
    :param userdata: 사용자 데이터
    :param msg: 수신된 메시지
    """
    global obstacle_detected
    if msg.topic == 'orin/ultrasonic':
        if msg.payload.decode() == '1':
            print("Obstacle detected!")
            obstacle_detected = True

def go_drive(pi_dir,bckwrd):

    global obstacle_detected, current_direction_index, obstacle_location, current_direction, back_drive
    obstacle_detected = False
    current_direction_index = 0
    obstacle_location = "unknown"
    current_direction = pi_dir  # 초기 방향 설정
    back_drive = bckwrd

    broker_address = "3.36.55.201"
    pi = mqtt.Client("Pi")
    pi.on_connect = on_connect
    pi.on_message = on_message
    pi.connect(broker_address, 1883)
    pi.loop_start()

    try:
        # JSON 파일에서 방향 데이터를 로드합니다.
        with open('directions.json', 'r') as f:
            directions_data = json.load(file)
            directions = directions_data['directions']
        
        # path.json 파일에서 경로 데이터를 로드
        with open('path.json', 'r') as file:
            path_data = json.load(file)

        directions = directions_data.get("directions", [])
        path = path_data.get("path", [])

        if not directions:
            raise ValueError("No directions found in directions.json")
        if not path:
            raise ValueError("No path found in path.json")

        # 서보 초기화
        kit = initialize_servo()

         # 종료 이벤트 생성
        stop_event = threading.Event()

        # 서보 제어 스레드 시작
        servo_thread = threading.Thread(target=control_servo, args=(kit, directions, stop_event))
        # 모터 제어 스레드 시작
        motor_thread = threading.Thread(target=control_motor, args=(directions, stop_event))

        servo_thread.start()
        motor_thread.start()
        
        while motor_thread.is_alive() and servo_thread.is_alive():
            if obstacle_detected:
                servo_thread.join()
                motor_thread.join()
                print("Stopping all motors due to obstacle detection.")
                setMotor(motor1, pwmA, 0, STOP)  # 모터 정지
                kit.servo[0].angle = direction_angles['C']  # 서보 초기 위치

                if (current_direction_index + 1) < len(path):
                    obstacle_location = path[current_direction_index + 1]
                else:
                    obstacle_location = "unknown"
                return {
                    'status': 'obstacle_detected',
                    'current_direction': current_direction,  # 현재 방향 추가
                    'obstacle_location': obstacle_location,
                    'current_location': path[current_direction_index]
                }
            time.sleep(1)

        servo_thread.join()
        motor_thread.join()

        print("All tasks completed.")
        return {'status': 'completed'}
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'status': 'error', 'message': str(e)}
    finally:
        stop_event.set()
        print("System stopped.")
        pi.loop_stop()
        pi.disconnect()