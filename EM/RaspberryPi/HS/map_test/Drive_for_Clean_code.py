import threading
import time
import json
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

# I2C 버스 설정 (SCL 및 SDA 핀을 사용하여 I2C 버스 초기화)
I2C_SCL_PIN = board.D1
I2C_SDA_PIN = board.D0
i2c_bus = busio.I2C(I2C_SCL_PIN, I2C_SDA_PIN)

def scan_i2c_bus(i2c):
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

def initialize_servo_kit():
    """
    PCA9685 PWM 드라이버를 초기화하고 ServoKit 인스턴스를 반환합니다.
    """
    try:
        print("Scanning I2C bus...")
        devices = scan_i2c_bus(i2c_bus)
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
DIRECTION_MAP = {
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
SERVO_ANGLES = {
    'C': 120,
    'L': 90,
    'R': 150,
    'LD': 105,
    'RD': 135
}

class PWMThrottleController:
    def __init__(self, pwm, channel):
        self.pwm = pwm
        self.channel = channel
        self.pwm.frequency = 60  # 주파수 설정

    def set_throttle(self, throttle):
        """
        모터의 스로틀을 설정합니다. 스로틀 값에 따라 방향과 속도가 결정됩니다.
        """
        pulse = int(0xFFFF * abs(throttle))
        if throttle > 0:
            self._set_forward(pulse)
        elif throttle < 0:
            self._set_backward(pulse)
        else:
            self._stop()

    def _set_forward(self, pulse):
        self.pwm.channels[self.channel + 5].duty_cycle = pulse
        self.pwm.channels[self.channel + 4].duty_cycle = 0
        self.pwm.channels[self.channel + 3].duty_cycle = 0xFFFF

    def _set_backward(self, pulse):
        self.pwm.channels[self.channel + 5].duty_cycle = pulse
        self.pwm.channels[self.channel + 4].duty_cycle = 0xFFFF
        self.pwm.channels[self.channel + 3].duty_cycle = 0

    def _stop(self):
        self.pwm.channels[self.channel + 5].duty_cycle = 0
        self.pwm.channels[self.channel + 4].duty_cycle = 0
        self.pwm.channels[self.channel + 3].duty_cycle = 0

# I2C 버스 설정 및 PWMThrottleController 인스턴스 생성
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60

# PWMThrottleController 인스턴스 생성
motor_controller = PWMThrottleController(pca, channel=0)

def control_motors(directions, path, stop_event):
    """
    주어진 방향과 경로에 따라 모터를 제어합니다.
    """
    try:
        current_direction = 'S'
        for i, (direction, coord) in enumerate(zip(directions, path)):
            if stop_event.is_set():
                break

            print(f"Current coordinate: {coord}")
            next_direction = directions[i + 1] if i + 1 < len(directions) else None
            
            if current_direction != direction:
                print("Slowing down for turn")
                motor_controller.set_throttle(0.5)
                time.sleep(3)

                angle = calculate_servo_angle(current_direction, direction)
                execute_turn(angle)
            else:
                if next_direction != None:
                    motor_controller.set_throttle(0.5)
                    time.sleep(1)
                else:
                    motor_controller.set_throttle(0.3)
                    time.sleep(1)

            current_direction = direction

        print("Reached the end of directions.")
    except:
        print("Motor control stopped.")
        stop_motors(stop_event)
    finally:
        print("Motor control stopped.")
        stop_motors(stop_event)

def execute_turn(angle):
    """
    지정된 각도에 따라 모터를 회전시키는 함수입니다.
    """
    if angle == 90 or angle == 150:
        motor_controller.set_throttle(-0.5)
        time.sleep(3)
        motor_controller.set_throttle(0.6)
        time.sleep(1)
    else:
        motor_controller.set_throttle(0.3)
        time.sleep(1)

def stop_motors(stop_event):
    """
    모터를 정지시키고 종료 이벤트를 설정합니다.
    """
    motor_controller.set_throttle(0)
    print("Motor control stopped.")
    stop_event.set()

def control_servos(kit, directions, stop_event):
    """
    서보 모터를 제어하여 방향에 따라 각도를 조절합니다.
    """
    current_direction = 'S'
    try:
        for i, direction in enumerate(directions):
            if stop_event.is_set():
                break

            next_direction = directions[i + 1] if i + 1 < len(directions) else None

            if current_direction != direction:
                angle = calculate_servo_angle(current_direction, direction)
                execute_servo_turn(kit, angle, current_direction, direction)
            else:
                kit.servo[0].angle = SERVO_ANGLES['C']
                time.sleep(1)

            current_direction = direction
        print("Completed all directions. Servo reset to center (120 degrees).")
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        kit.servo[0].angle = SERVO_ANGLES['C']
        stop_event.set()
    

def execute_servo_turn(kit, angle,current_direction, direction):
    """
    서보 모터를 지정된 각도로 회전시키는 함수입니다.
    """
    if angle in (90, 150):
        kit.servo[0].angle = angle
        time.sleep(3)
        angle = calculate_servo_angle(direction,current_direction)
        kit.servo[0].angle = angle
        time.sleep(3)
        kit.servo[0].angle = SERVO_ANGLES['C']
        time.sleep(1)
    else:
        if angle > 120:
            angle = 150
        elif angle < 120:
            angle = 90
              
        kit.servo[0].angle = angle
        time.sleep(2)
        kit.servo[0].angle = SERVO_ANGLES['C']
        time.sleep(2)

def calculate_servo_angle(current_direction, target_direction):
    """
    현재 방향과 목표 방향에 따라 서보 각도를 결정합니다.
    """
    direction_pair = (current_direction, target_direction)
    angle_map = {
        ('N', 'W'): SERVO_ANGLES['L'],
        ('N', 'E'): SERVO_ANGLES['R'],
        ('N', 'H'): SERVO_ANGLES['LD'],
        ('N', 'J'): SERVO_ANGLES['RD'],
        ('S', 'E'): SERVO_ANGLES['L'],
        ('S', 'W'): SERVO_ANGLES['R'],
        ('S', 'X'): SERVO_ANGLES['LD'],
        ('S', 'Z'): SERVO_ANGLES['RD'],
        ('E', 'N'): SERVO_ANGLES['L'],
        ('E', 'S'): SERVO_ANGLES['R'],
        ('E', 'J'): SERVO_ANGLES['LD'],
        ('E', 'X'): SERVO_ANGLES['RD'],
        ('W', 'S'): SERVO_ANGLES['L'],
        ('W', 'N'): SERVO_ANGLES['R'],
        ('W', 'H'): SERVO_ANGLES['RD'],
        ('W', 'Z'): SERVO_ANGLES['LD'],
        ('H', 'N'): SERVO_ANGLES['RD'],
        ('H', 'J'): SERVO_ANGLES['R'],
        ('H', 'W'): SERVO_ANGLES['LD'],
        ('H', 'Z'): SERVO_ANGLES['L'],
        ('J', 'E'): SERVO_ANGLES['RD'],
        ('J', 'X'): SERVO_ANGLES['R'],
        ('J', 'N'): SERVO_ANGLES['LD'],
        ('J', 'H'): SERVO_ANGLES['L'],
        ('Z', 'S'): SERVO_ANGLES['LD'],
        ('Z', 'H'): SERVO_ANGLES['R'],
        ('Z', 'W'): SERVO_ANGLES['RD'],
        ('Z', 'X'): SERVO_ANGLES['L'],
        ('X', 'J'): SERVO_ANGLES['L'],
        ('X', 'Z'): SERVO_ANGLES['R'],
        ('X', 'E'): SERVO_ANGLES['LD'],
        ('X', 'S'): SERVO_ANGLES['RD'],
    }
    return angle_map.get(direction_pair, None)

if __name__ == "__main__":
    # JSON 파일에서 방향 및 경로 데이터를 로드합니다.
    with open('directions.json', 'r') as file:
        directions_data = json.load(file)
        directions = directions_data['directions']

    with open('path.json', 'r') as file:
        path_data = json.load(file)
        path = path_data['path']

    stop_event = threading.Event()

    try:
        # 서보 초기화
        servo_kit = initialize_servo_kit()

        # 서보 제어 스레드 시작
        servo_thread = threading.Thread(target=control_servos, args=(servo_kit, directions, stop_event))
        # 모터 제어 스레드 시작
        motor_thread = threading.Thread(target=control_motors, args=(directions, path, stop_event))

        servo_thread.start()
        motor_thread.start()

        servo_thread.join()
        motor_thread.join()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        stop_event.set()
