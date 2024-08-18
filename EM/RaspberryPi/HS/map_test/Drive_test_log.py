import threading
import time
import json
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

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
    'L': 90,        # 좌회전
    'R': 150,       # 우회전
    'LD': 105,      # 좌대각선
    'RD': 135       # 우대각선
}

class PWMThrottleHat:
    def __init__(self, pwm, channel):
        self.pwm = pwm
        self.channel = channel
        self.pwm.frequency = 60  # 주파수 설정

    def set_throttle(self, throttle):
        pulse = int(0xFFFF * abs(throttle))

        if throttle > 0:
            self.pwm.channels[self.channel + 5].duty_cycle = pulse
            self.pwm.channels[self.channel + 4].duty_cycle = 0
            self.pwm.channels[self.channel + 3].duty_cycle = 0xFFFF
        elif throttle < 0:
            self.pwm.channels[self.channel + 5].duty_cycle = pulse
            self.pwm.channels[self.channel + 4].duty_cycle = 0xFFFF
            self.pwm.channels[self.channel + 3].duty_cycle = 0
        else:
            self.pwm.channels[self.channel + 5].duty_cycle = 0
            self.pwm.channels[self.channel + 4].duty_cycle = 0
            self.pwm.channels[self.channel + 3].duty_cycle = 0

# I2C 버스 설정
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60  # PCA9685 주파수 설정

# PWMThrottleHat 인스턴스 생성
motor_hat = PWMThrottleHat(pca, channel=0)

def control_motor(directions, path, stop_event):
    """
    모터를 제어하여 방향에 따라 전진 및 후진을 수행하고, 좌표를 출력하는 함수
    :param directions: 방향 리스트
    :param path: 좌표 리스트
    :param stop_event: 종료 이벤트
    """
    try:
        current_direction = 'S'  # 초기 방향 설정
        for i, (direction, coord) in enumerate(zip(directions, path)):
            if stop_event.is_set():
                break

            # 좌표 출력
            print(f"Current coordinate: {coord}")

            # 다음 방향 계산
            next_direction = directions[i + 1] if i + 1 < len(directions) else None
            
            if current_direction != direction:
                print("Slowing down for turn")
                motor_hat.set_throttle(0.5)  # 방향 전환 전 속도 줄이기
                time.sleep(3)

                angle = get_servo_angle(current_direction, direction)
                if angle == 90:
                    motor_hat.set_throttle(-0.5)
                    time.sleep(3)
                    motor_hat.set_throttle(0.6)
                    time.sleep(1)
                elif angle == 150:
                    motor_hat.set_throttle(-0.5)
                    time.sleep(3)
                    motor_hat.set_throttle(0.6)
                    time.sleep(1)
                else:
                    if angle > 120:
                        motor_hat.set_throttle(0.3)
                        time.sleep(1)
                    elif angle < 120:
                        motor_hat.set_throttle(0.3)
                        time.sleep(1)
            else:
                if next_direction != None:
                    if direction != next_direction:
                        motor_hat.set_throttle(0.5)  # 전진 50% 속도    
                        time.sleep(1)
                    else:
                        motor_hat.set_throttle(0.5)  # 전진 50% 속도
                        time.sleep(1)  # 서보와 동기화
                else:
                    motor_hat.set_throttle(0.3)  # 전진 50% 속도    
                    time.sleep(1)  # 서보와 동기화

            # 현재 방향 업데이트
            current_direction = direction

        print("Reached the end of directions.")
    except KeyboardInterrupt:
        stop_event.set()  # 종료 이벤트 설정
    finally:
        motor_hat.set_throttle(0)  # 모터 정지
        print("Motor control stopped.")
        stop_event.set()

def control_servo(kit, directions, stop_event):
    """
    서보 모터를 제어하여 방향에 따라 각도를 조절하는 함수
    :param kit: ServoKit 인스턴스
    :param directions: 방향 리스트
    :param stop_event: 종료 이벤트
    """
    try:
        current_direction = 'S'
        for i, direction in enumerate(directions):
            if stop_event.is_set():
                break

            next_direction = directions[i + 1] if i + 1 < len(directions) else None

            if current_direction == direction:
                kit.servo[0].angle = direction_angles['C']
                print(f"Current direction is {current_direction}. Servo reset to center (110 degrees).")
                if next_direction != None:
                    if direction != next_direction:
                        time.sleep(1)
                    else:
                        time.sleep(1.5)
            else:
                angle = get_servo_angle(current_direction, direction)
                if angle is not None:
                    print(f"Servo set to {direction} direction ({angle} degrees)")

                    if angle == 90:
                        kit.servo[0].angle = angle
                        time.sleep(3)
                        angle = get_servo_angle(direction, current_direction)
                        kit.servo[0].angle = angle
                        print(f"Servo set to backward")
                        time.sleep(3)
                        kit.servo[0].angle = direction_angles['C']
                        time.sleep(1)
                    elif angle == 150:
                        kit.servo[0].angle = angle
                        time.sleep(3)
                        angle = get_servo_angle(direction, current_direction)
                        kit.servo[0].angle = angle
                        print(f"Servo set to backward")
                        time.sleep(3)
                        kit.servo[0].angle = direction_angles['C']
                        time.sleep(1)
                    else:
                        if angle > 120:
                            angle = 150
                        elif angle < 120:
                            angle = 90    

                        if angle==150:
                            kit.servo[0].angle = angle
                            time.sleep(2)
                            kit.servo[0].angle = direction_angles['C']
                            time.sleep(2)
                        elif angle==90:
                            kit.servo[0].angle = angle
                            time.sleep(2)
                            kit.servo[0].angle = direction_angles['C']
                            time.sleep(2)
                        
            current_direction = direction  # 현재 방향 업데이트

        kit.servo[0].angle = direction_angles['C']
        print("Completed all directions. Servo reset to center (110 degrees).")
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
        elif target_direction == 'J':
            return direction_angles['LD']
        elif target_direction == 'X':
            return direction_angles['RD']
    elif current_direction == 'W':
        if target_direction == 'S':
            return direction_angles['L']
        elif target_direction == 'N':
            return direction_angles['R']
        elif target_direction == 'H':
            return direction_angles['RD']
        elif target_direction == 'Z':
            return direction_angles['LD']
    elif current_direction == 'H':
        if target_direction == 'N':
            return direction_angles['RD']
        elif target_direction == 'J':
            return direction_angles['R']
        elif target_direction == 'W':
            return direction_angles['LD']
        elif target_direction == 'Z':
            return direction_angles['L']
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
        elif target_direction == 'H':
            return direction_angles['R']
        elif target_direction == 'W':
            return direction_angles['RD']
        elif target_direction == 'X':
            return direction_angles['L']
    elif current_direction == 'X':
        if target_direction == 'J':
            return direction_angles['L']
        elif target_direction == 'Z':
            return direction_angles['R']
        elif target_direction == 'E':
            return direction_angles['LD']
        elif target_direction == 'S':
            return direction_angles['RD']
    return None

if __name__ == "__main__":
    # JSON 파일에서 방향 및 경로 데이터를 로드합니다.
    with open('directions.json', 'r') as f:
        data = json.load(f)
        directions = data['directions']

    with open('path.json', 'r') as f:
        path_data = json.load(f)
        path = path_data['path']

    stop_event = threading.Event()

    try:
        # 서보 초기화
        kit = initialize_servo()

        # 서보 제어 스레드 시작
        servo_thread = threading.Thread(target=control_servo, args=(kit, directions, stop_event))
        # 모터 제어 스레드 시작
        motor_thread = threading.Thread(target=control_motor, args=(directions, path, stop_event))

        servo_thread.start()
        motor_thread.start()
        
        servo_thread.join()
        motor_thread.join()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        stop_event.set()
