import threading
import time
import json
import board
import busio
from adafruit_servokit import ServoKit
from adafruit_pca9685 import PCA9685
import paho.mqtt.client as mqtt

# I2C 버스 설정 (SCL 및 SDA 핀을 사용하여 I2C 버스 초기화)
SCL_PIN = board.D1  # GPIO 1
SDA_PIN = board.D0  # GPIO 0
i2c_bus = busio.I2C(SCL_PIN, SDA_PIN)

def i2c_scan(i2c):
    """
    I2C 버스를 스캔하여 연결된 모든 I2C 장치의 주소를 반환합니다.
    :param i2c: I2C 버스 객체
    :return: I2C 장치 주소의 리스트
    """
    while not i2c.try_lock():  # I2C 버스를 사용할 수 있을 때까지 대기
        pass
    try:
        devices = i2c.scan()  # 연결된 모든 I2C 장치 스캔
        return devices
    finally:
        i2c.unlock()  # 사용 후 I2C 버스 잠금 해제

def initialize_servo():
    """
    PCA9685 서보 컨트롤러를 초기화합니다.
    :return: 초기화된 ServoKit 객체
    :raises: ValueError, Exception
    """
    try:
        print("Scanning I2C bus...")
        devices = i2c_scan(i2c_bus)  # I2C 버스 스캔
        print(f"I2C devices found: {[hex(device) for device in devices]}")

        if not devices:
            raise ValueError("No I2C devices found on the bus.")  # I2C 장치가 없을 경우 예외 발생

        # PCA9685 컨트롤러 초기화
        kit = ServoKit(channels=16, i2c=i2c_bus, address=0x60)
        print("PCA9685 initialized at address 0x60.")
        return kit
    except Exception as e:
        print(f"Error initializing PCA9685: {e}")  # 초기화 중 오류 발생 시 메시지 출력
        raise

class PWMThrottleHat:
    def __init__(self, pwm, channel):
        """
        PWMThrottleHat 초기화
        :param pwm: PCA9685 PWM 객체
        :param channel: PWM 채널
        """
        self.pwm = pwm
        self.channel = channel
        self.pwm.frequency = 60  # 주파수 설정

    def set_throttle(self, throttle):
        """
        모터의 스로틀 값을 설정합니다.
        :param throttle: 스로틀 값 (-1.0 ~ 1.0)
        """
        pulse = int(0xFFFF * abs(throttle))  # 16비트 듀티 사이클 계산

        if throttle > 0:
            self.pwm.channels[self.channel + 5].duty_cycle = pulse  # 전진
            self.pwm.channels[self.channel + 4].duty_cycle = 0
            self.pwm.channels[self.channel + 3].duty_cycle = 0xFFFF
        elif throttle < 0:
            self.pwm.channels[self.channel + 5].duty_cycle = pulse  # 후진
            self.pwm.channels[self.channel + 4].duty_cycle = 0xFFFF
            self.pwm.channels[self.channel + 3].duty_cycle = 0
        else:
            self.pwm.channels[self.channel + 5].duty_cycle = 0  # 정지
            self.pwm.channels[self.channel + 4].duty_cycle = 0
            self.pwm.channels[self.channel + 3].duty_cycle = 0

# I2C 버스 및 PCA9685 초기화
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60

# PWMThrottleHat 초기화 (채널 0 사용)
motor_hat = PWMThrottleHat(pca, channel=0)

# 방향 매핑 및 서보 각도 설정
directions_mapping = {
    (-1, 0): 'N',
    (1, 0): 'S',
    (0, -1): 'W',
    (0, 1): 'E',
    (-1, -1): 'H',
    (-1, 1): 'J',
    (1, -1): 'Z',
    (1, 1): 'X'
}

# 각 방향에 대한 서보 각도 매핑
direction_angles = {
    'C': 110,  # 센터
    'L': 30,   # 왼쪽
    'R': 180,  # 오른쪽
    'LD': 70,  # 왼쪽 대각선
    'RD': 140  # 오른쪽 대각선
}

# 전역 변수로 인덱스 및 장애물 감지 상태 저장
current_direction_index = 0
obstacle_detected = False
obstacle_location = "unknown"
current_direction = 'S'  # 현재 방향을 추적하기 위한 변수

def control_motor(directions, stop_event, path):
    """
    모터를 제어하며 주어진 방향에 따라 이동합니다. 장애물이 감지되면 제어를 중지합니다.
    :param directions: 방향 리스트
    :param stop_event: 중지 이벤트 객체
    :param path: 경로 리스트
    """
    global current_direction_index, obstacle_detected, current_direction
    try:
        current_direction = 'S'
        for i, direction in enumerate(directions):
            if obstacle_detected:
                break

            current_direction_index = i  # 현재 방향 인덱스 업데이트

            if current_direction != direction:
                print("Slowing down for turn")
                motor_hat.set_throttle(0.2)  # 방향 전환을 위해 속도 줄임
                time.sleep(1)

            if (current_direction == 'N' and direction in ['Z', 'X']) or (current_direction == 'S' and direction in ['H', 'J']):
                print("Moving backward for diagonal direction")
                motor_hat.set_throttle(-0.5)  # 대각선 방향을 위해 후진
                time.sleep(2)
            else:
                motor_hat.set_throttle(0.5)  # 전진
                time.sleep(2)

            if current_direction != direction:
                print("Resuming normal speed")
                motor_hat.set_throttle(0.5)  # 전환 후 정상 속도로 복귀
                time.sleep(2)

            current_direction = direction  # 현재 방향 업데이트

        print("Reached the end of directions.")
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        motor_hat.set_throttle(0)  # 모터 정지
        print("Motor control stopped.")
        stop_event.set()

def control_servo(kit, directions, stop_event):
    """
    서보 모터를 제어하며 주어진 방향에 따라 회전합니다. 장애물이 감지되면 제어를 중지합니다.
    :param kit: ServoKit 객체
    :param directions: 방향 리스트
    :param stop_event: 중지 이벤트 객체
    """
    global current_direction_index, current_direction
    try:
        current_direction = 'S'
        for direction in directions:
            if obstacle_detected:
                break

            if current_direction == direction:
                kit.servo[0].angle = direction_angles['C']  # 현재 방향일 경우 서보를 중앙으로 설정
                print(f"Current direction is {current_direction}. Servo reset to center (110 degrees).")
                time.sleep(1)
            else:
                angle = get_servo_angle(current_direction, direction)
                if angle is not None:
                    kit.servo[0].angle = angle
                    print(f"Servo set to {direction} direction ({angle} degrees)")
                    time.sleep(1.5)

            current_direction = direction  # 현재 방향 업데이트

        kit.servo[0].angle = direction_angles['C']
        print("Completed all directions. Servo reset to center (110 degrees).")
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        kit.servo[0].angle = direction_angles['C']
        print("Servo control stopped.")
        stop_event.set()

def get_servo_angle(current_direction, target_direction):
    """
    현재 방향과 목표 방향에 따라 서보 각도를 계산합니다.
    :param current_direction: 현재 방향
    :param target_direction: 목표 방향
    :return: 서보 각도
    """
    if current_direction == 'N':
        if target_direction == 'W':
            return direction_angles['L']
        elif target_direction == 'E':
            return direction_angles['R']
        elif target_direction == 'H':
            return direction_angles['LD']
        elif target_direction == 'J':
            return direction_angles['RD']
    elif current_direction == 'S':
        if target_direction == 'E':
            return direction_angles['L']
        elif target_direction == 'W':
            return direction_angles['R']
        elif target_direction == 'X':
            return direction_angles['LD']
        elif target_direction == 'Z':
            return direction_angles['RD']
    elif current_direction == 'E':
        if target_direction == 'N':
            return direction_angles['L']
        elif target_direction == 'S':
            return direction_angles['R']
        elif target_direction == 'H':
            return direction_angles['RD']
        elif target_direction == 'X':
            return direction_angles['LD']
    elif current_direction == 'W':
        if target_direction == 'N':
            return direction_angles['R']
        elif target_direction == 'S':
            return direction_angles['L']
        elif target_direction == 'J':
            return direction_angles['LD']
        elif target_direction == 'Z':
            return direction_angles['RD']
    elif current_direction == 'H':
        if target_direction == 'N':
            return direction_angles['RD']
        elif target_direction == 'J':
            return direction_angles['R']
        elif target_direction == 'W':
            return direction_angles['L']
        elif target_direction == 'S':
            return direction_angles['LD']
    elif current_direction == 'J':
        if target_direction == 'E':
            return direction_angles['RD']
        elif target_direction == 'X':
            return direction_angles['R']
        elif target_direction == 'N':
            return direction_angles['LD']
        elif target_direction == 'H':
            return direction_angles['L']
    elif current_direction == 'Z':
        if target_direction == 'S':
            return direction_angles['LD']
        elif target_direction == 'X':
            return direction_angles['L']
        elif target_direction == 'W':
            return direction_angles['RD']
        elif target_direction == 'H':
            return direction_angles['R']
    elif current_direction == 'X':
        if target_direction == 'S':
            return direction_angles['RD']
        elif target_direction == 'Z':
            return direction_angles['R']
        elif target_direction == 'E':
            return direction_angles['LD']
        elif target_direction == 'J':
            return direction_angles['L']
    else:
        return direction_angles['C']

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

def go_drive():
    """
    전체 운전 프로세스를 관리하는 함수
    :return: 작업 상태를 나타내는 딕셔너리
    """
    global obstacle_detected, current_direction_index, obstacle_location, current_direction
    obstacle_detected = False
    current_direction_index = 0
    obstacle_location = "unknown"
    current_direction = 'S'  # 초기 방향 설정

    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message
    mqtt_client.connect("mqtt_broker_url")  # MQTT 브로커 URL로 변경하세요
    mqtt_client.subscribe("orin/ultrasonic")
    mqtt_client.loop_start()

    try:
        # JSON 파일에서 방향 및 경로 데이터 로드
        with open('directions.json', 'r') as file:
            directions_data = json.load(file)

        with open('path.json', 'r') as file:
            path_data = json.load(file)

        directions = directions_data.get("directions", [])
        path = path_data.get("path", [])

        if not directions:
            raise ValueError("No directions found in directions.json")
        if not path:
            raise ValueError("No path found in path.json")

        # 서보 모터 초기화
        kit = initialize_servo()
        stop_event = threading.Event()

        # 모터와 서보 제어를 위한 스레드 시작
        motor_thread = threading.Thread(target=control_motor, args=(directions, stop_event, path))
        servo_thread = threading.Thread(target=control_servo, args=(kit, directions, stop_event))

        motor_thread.start()
        servo_thread.start()

        while motor_thread.is_alive() and servo_thread.is_alive():
            if obstacle_detected:
                print("Stopping all motors due to obstacle detection.")
                motor_hat.set_throttle(0)  # 모터 속도 0으로 설정
                kit.servo[0].angle = direction_angles['C']  # 서보 모터를 센터로 이동

                if (current_direction_index + 1) < len(path):
                    obstacle_location = path[current_direction_index + 1]
                else:
                    obstacle_location = "unknown"

                return {
                    'status': 'obstacle_detected',
                    'current_direction': current_direction,  # 현재 방향 추가
                    'obstacle_location': obstacle_location
                }
            time.sleep(1)

        motor_thread.join()
        servo_thread.join()
        print("All tasks completed.")
        return {'status': 'completed'}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {'status': 'error', 'message': str(e)}
    finally:
        stop_event.set()  # 모든 스레드 종료
        motor_hat.set_throttle(0)  # 모터 속도 0으로 설정
        kit.servo[0].angle = direction_angles['C']  # 서보 모터를 센터로 이동
        print("System stopped.")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()