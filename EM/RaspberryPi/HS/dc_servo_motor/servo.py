import threading
import time
import json
import board
import busio
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
    'C': 110,       # 중앙
    'L': 30,        # 좌회전
    'R': 180,       # 우회전
    'LD': 70,       # 좌대각선
    'RD': 140       # 우대각선
}

def control_servo(kit, directions, stop_event):
    """
    서보 모터를 제어하여 방향에 따라 각도를 조절하는 함수
    :param kit: ServoKit 인스턴스
    :param directions: 방향 리스트
    :param stop_event: 종료 이벤트
    """
    try:
        current_direction = 'S'
        for direction in directions:
            if stop_event.is_set():
                break

            # 현재 방향과 목표 방향이 같으면 서보를 중앙으로 설정
            if current_direction == direction:
                kit.servo[0].angle = direction_angles['C']
                print(f"Current direction is {current_direction}. Servo reset to center (110 degrees).")
                time.sleep(1)  # 중앙으로 이동 후 대기
            else:
                # 방향 매핑을 통해 현재 방향과 목표 방향을 결정
                angle = get_servo_angle(current_direction, direction)
                if angle is not None:
                    kit.servo[0].angle = angle
                    print(f"Servo set to {direction} direction ({angle} degrees)")
                    time.sleep(1.5)  # 서보 위치 유지 시간

            current_direction = direction  # 현재 방향 업데이트

        # 모든 방향이 완료된 후 서보를 중앙으로 복귀
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
        return direction_angles['C']  # 기본 중앙 각도

def main():
    try:
        # 서보 모터 초기화
        kit = initialize_servo()

        # directions.json 파일에서 방향 데이터를 로드
        with open('directions.json', 'r') as file:
            directions_data = json.load(file)

        # 방향 리스트 가져오기
        directions = directions_data.get("directions", [])

        if not directions:
            raise ValueError("No directions found in directions.json.")

        # 종료 이벤트 설정
        stop_event = threading.Event()

        # 서보 제어 쓰레드 시작
        servo_thread = threading.Thread(target=control_servo, args=(kit, directions, stop_event))
        servo_thread.start()

        # 쓰레드가 완료될 때까지 대기
        servo_thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
