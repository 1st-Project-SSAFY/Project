import threading
import time
import json
import board
import busio
import sys
import os
import importlib
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
import paho.mqtt.client as mqtt
import subprocess
#BLE 삼변측량 파일 실행
scr_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'.../SDL_Pi_iBeaconScanner'))
ble_module = 'location4'

# I2C 버스 설정 (SCL 및 SDA 핀을 사용하여 I2C 버스 초기화)
I2C_SCL_PIN = board.D1
I2C_SDA_PIN = board.D0
i2c_bus = busio.I2C(I2C_SCL_PIN, I2C_SDA_PIN)

# 종료 이벤트 객체 생성
stop_event = threading.Event()

robot_data ={
    "info": {
        "mission": 1,
        "location_x": 0,
        "location_y": 0,
        "block_x": None,
        "block_y": None
    }
}

robot_data['info']['mission']

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

#좌표 매핑
GRID_MAP = {
    'N':(-1, 0) ,  # 북쪽
    'S':(1, 0),   # 남쪽
    'W':(0, -1),  # 서쪽
    'E':(0, 1),   # 동쪽
    'H':(-1, -1), # 북서쪽
    'J':(-1, 1),  # 북동쪽
    'Z':(1, -1),  # 남서쪽
    'X':(1, 1)    # 남동쪽
}

# 서보 각도 매핑
SERVO_ANGLES = {
    'C': 122,
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
    global cdir, current_direction_index, obstacle_detected, back_drive
    current_direction = cdir
    Drive_Mode = 1
    if back_drive == 1:
        Drive_Mode = -1

    try:
        for current_direction_index, (direction, coord) in enumerate(zip(directions, path)):
            '''if stop_event.is_set():
                break'''

            robot_data['info']['location_x'] =  coord[0]
            robot_data['info']['location_y'] =  coord[1]
            robot_data['info']['mission'] = 'working'

            # JSON 파일로 저장하기
            with open('robot_data.json', 'w') as json_file:
                json.dump(robot_data, json_file, indent=4)

            if obstacle_detected:
                stop_event.is_set()
                return
                

            print(f"Current coordinate: {coord}")
            next_direction = directions[current_direction_index + 1] if current_direction_index + 1 < len(directions) else None
            
            if current_direction != direction:
                print("Slowing down for turn")
                if Drive_Mode==1:
                    motor_controller.set_throttle(0.5*Drive_Mode)
                else:
                    motor_controller.set_throttle(0.6*Drive_Mode)
                
                time.sleep(3)
                
                angle = calculate_servo_angle(current_direction, direction)
                execute_turn(angle,Drive_Mode)
            else:
                if next_direction != None:
                    if Drive_Mode == 1:
                        motor_controller.set_throttle(0.4*Drive_Mode)
                    else:
                        motor_controller.set_throttle(0.4*Drive_Mode)
                    time.sleep(2)
                else:
                    if Drive_Mode ==1:
                        motor_controller.set_throttle(0.6*Drive_Mode)
                    else:
                        motor_controller.set_throttle(0.6*Drive_Mode)
                    
                    time.sleep(2)

            current_direction = direction
            cdir = current_direction

        print("Reached the end of directions.")
    except:
        print("Motor control stopped.")
        stop_motors(stop_event)
    finally:
        print("Motor control stopped.")
        stop_motors(stop_event)

def execute_turn(angle,Drive_Mode):
    """
    지정된 각도에 따라 모터를 회전시키는 함수입니다.
    """
    if angle == 90 or angle == 150:
        if Drive_Mode == 1:
            motor_controller.set_throttle(-0.6*Drive_Mode)
        else:
            motor_controller.set_throttle(-0.6*Drive_Mode)
        time.sleep(3)
        if Drive_Mode == 1:
            motor_controller.set_throttle(0.7*Drive_Mode)
        else:
            motor_controller.set_throttle(-0.6*Drive_Mode)
        time.sleep(1)
    else:
        if Drive_Mode == 1:
            motor_controller.set_throttle(0.4*Drive_Mode)
        else:
            motor_controller.set_throttle(0.5*Drive_Mode)
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
    global cdir, obstacle_detected
    current_direction = cdir
    try:
        for current_direction_index, direction in enumerate(directions):
            '''if stop_event.is_set():
                break'''

            if obstacle_detected:
                stop_event.is_set()
                return
            
            print(f"Direction:{direction}")

            #next_direction = directions[i + 1] if i + 1 < len(directions) else None

            if current_direction != direction:
                angle = calculate_servo_angle(current_direction, direction)
                execute_servo_turn(kit, angle, current_direction, direction)
            else:
                kit.servo[0].angle = SERVO_ANGLES['C']
                time.sleep(1)

            current_direction = direction
            cdir = current_direction
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
        if angle > 122:
            angle = 150
        elif angle < 122:
            angle = 90
              
        kit.servo[0].angle = angle
        time.sleep(1)
        kit.servo[0].angle = SERVO_ANGLES['C']
        time.sleep(3)

def calculate_servo_angle(current_direction, target_direction):
    """
    현재 방향과 목표 방향에 따라 서보 각도를 결정합니다.
    """
    angle_map = {
        # back_drive == 0
        ('N', 'W'): SERVO_ANGLES['L'],
        ('N', 'E'): SERVO_ANGLES['R'],
        ('N', 'H'): SERVO_ANGLES['LD'],
        ('N', 'J'): SERVO_ANGLES['RD'],
        ('N', 'X'): SERVO_ANGLES['LD'],
        ('N', 'Z'): SERVO_ANGLES['RD'],
        ('N', 'S'): SERVO_ANGLES['C'],
        ('N', 'N'): SERVO_ANGLES['C'],

        ('S', 'E'): SERVO_ANGLES['L'],
        ('S', 'W'): SERVO_ANGLES['R'],
        ('S', 'X'): SERVO_ANGLES['LD'],
        ('S', 'Z'): SERVO_ANGLES['RD'],
        ('S', 'H'): SERVO_ANGLES['LD'],
        ('S', 'J'): SERVO_ANGLES['RD'],
        ('S', 'S'): SERVO_ANGLES['C'],
        ('S', 'N'): SERVO_ANGLES['C'],

        ('E', 'N'): SERVO_ANGLES['L'],
        ('E', 'S'): SERVO_ANGLES['R'],
        ('E', 'J'): SERVO_ANGLES['LD'],
        ('E', 'X'): SERVO_ANGLES['RD'],
        ('E', 'H'): SERVO_ANGLES['RD'],
        ('E', 'Z'): SERVO_ANGLES['LD'],
        ('E', 'E'): SERVO_ANGLES['C'],
        ('E', 'W'): SERVO_ANGLES['C'],

        ('W', 'S'): SERVO_ANGLES['L'],
        ('W', 'N'): SERVO_ANGLES['R'],
        ('W', 'H'): SERVO_ANGLES['RD'],
        ('W', 'Z'): SERVO_ANGLES['LD'],
        ('W', 'J'): SERVO_ANGLES['LD'],
        ('W', 'X'): SERVO_ANGLES['RD'],
        ('W', 'E'): SERVO_ANGLES['C'],
        ('W', 'W'): SERVO_ANGLES['C'],
        

        ('H', 'N'): SERVO_ANGLES['RD'],
        ('H', 'J'): SERVO_ANGLES['R'],
        ('H', 'W'): SERVO_ANGLES['LD'],
        ('H', 'Z'): SERVO_ANGLES['L'],
        ('H', 'E'): SERVO_ANGLES['LD'],
        ('H', 'S'): SERVO_ANGLES['RD'],
        ('H', 'H'): SERVO_ANGLES['C'],
        ('H', 'X'): SERVO_ANGLES['C'],

        ('X', 'J'): SERVO_ANGLES['L'],
        ('X', 'Z'): SERVO_ANGLES['R'],
        ('X', 'E'): SERVO_ANGLES['LD'],
        ('X', 'S'): SERVO_ANGLES['RD'],
        ('X', 'W'): SERVO_ANGLES['LD'],
        ('X', 'N'): SERVO_ANGLES['RD'],
        ('X', 'H'): SERVO_ANGLES['C'],
        ('X', 'H'): SERVO_ANGLES['C'],

        ('J', 'H'): SERVO_ANGLES['L'],
        ('J', 'X'): SERVO_ANGLES['R'],
        ('J', 'N'): SERVO_ANGLES['LD'],
        ('J', 'E'): SERVO_ANGLES['RD'],
        ('J', 'W'): SERVO_ANGLES['RD'],
        ('J', 'S'): SERVO_ANGLES['LD'],
        ('J', 'J'): SERVO_ANGLES['C'],
        ('J', 'Z'): SERVO_ANGLES['C'],
        
        ('Z', 'W'): SERVO_ANGLES['RD'],
        ('Z', 'S'): SERVO_ANGLES['LD'],
        ('Z', 'H'): SERVO_ANGLES['R'],
        ('Z', 'X'): SERVO_ANGLES['L'],
        ('Z', 'N'): SERVO_ANGLES['LD'],
        ('Z', 'E'): SERVO_ANGLES['RD'],
        ('Z', 'Z'): SERVO_ANGLES['C'],
        ('Z', 'J'): SERVO_ANGLES['C'],
    }

    # 방향 조합에 따른 각도 반환 (back_drive == 1인 경우 반대로 반환)
    direction_pair = (current_direction, target_direction)
    if back_drive == 1:
        # 방향에 따른 각도 맵에서 반대 각도를 반환
        reverse_angle_map = {
            SERVO_ANGLES['L']: SERVO_ANGLES['R'],
            SERVO_ANGLES['R']: SERVO_ANGLES['L'],
            SERVO_ANGLES['LD']: SERVO_ANGLES['RD'],
            SERVO_ANGLES['RD']: SERVO_ANGLES['LD'],
            SERVO_ANGLES['C'] : SERVO_ANGLES['C']
        }
        return reverse_angle_map.get(angle_map.get(direction_pair, None), None)
    else:
        return angle_map.get(direction_pair, None)



def on_connect(client, userdata, flags, rc):
    """
    MQTT 서버에 연결되었을 때 호출되는 콜백 함수
    :param client: MQTT 클라이언트 객체
    :param userdata: 사용자 데이터
    :param flags: 플래그
    :param rc: 연결 상태 코드
    """
    global back_drive

    print("Connected!")
    client.subscribe("ultrasonic/detect/object")

def on_message(client, userdata, msg):
    """
    MQTT 메시지를 수신했을 때 호출되는 콜백 함수
    :param client: MQTT 클라이언트 객체
    :param userdata: 사용자 데이터
    :param msg: 수신된 메시지
    """
    global obstacle_detected
    if msg.topic == 'ultrasonic/detect/object' and msg.payload.decode() == '1':
        print("Obstacle detected!")
        obstacle_detected = True

def run_module(module_name, module_path):
    # 모듈 경로를 sys.path에 추가합니다.
    sys.path.append(module_path)
    
    # 모듈을 가져옵니다.
    module = importlib.import_module(module_name)
    
    # 모듈의 main() 함수를 호출합니다 (모듈에 main() 함수가 있는 경우)
    '''if hasattr(module, 'main'):
        module.main()
    else:
        print(f"{module_name} does not have a main() function.")'''

def go_drive(initial_direction, backward):
    """
    모터와 서보를 제어하여 주어진 방향으로 이동합니다.
    :param initial_direction: 초기 방향
    :param backward: 후진 여부
    :return: 결과 딕셔너리
    """

    global obstacle_detected, cdir, back_drive, current_direction_index

    # 전역 변수 초기화
    obstacle_detected = False
    cdir = initial_direction
    back_drive = backward
    current_direction_index = 0

    # MQTT 브로커 주소 및 클라이언트 설정
    broker_address = "3.36.55.201"
    #broker_address = "43.201.10.191"
    mqtt_client = mqtt.Client("Pi")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(broker_address, 1883)

    mqtt_client.loop_start()

    if back_drive == 1:
        print("Driving backward")
        mqtt_client.publish("ultrasonic/select","backward")
    else :
        print("Driving Forward")
        mqtt_client.publish("ultrasonic/select","forward")
        

    try:

        # JSON 파일에서 방향 및 경로 데이터 로드
        with open('directions.json', 'r') as file:
            directions_data = json.load(file)
            directions = directions_data.get('directions', [])

        with open('path.json', 'r') as file:
            path_data = json.load(file)
            path = path_data.get('path', [])

        if not directions:
            raise ValueError("No directions found in directions.json")
        if not path:
            raise ValueError("No path found in path.json")

        # 서보 초기화
        servo_kit = initialize_servo_kit()

        # 서보 제어 스레드 시작
        servo_thread = threading.Thread(target=control_servos, args=(servo_kit, directions, stop_event))
        # 모터 제어 스레드 시작
        motor_thread = threading.Thread(target=control_motors, args=(directions, path, stop_event))

        print("Start Thread")

        servo_thread.start()
        motor_thread.start()

        while motor_thread.is_alive() and servo_thread.is_alive():
            if obstacle_detected:
                
                #run_module(ble_module,scr_path)
                

                servo_thread.join()  # 서보 제어 스레드 종료
                motor_thread.join()  # 모터 제어 스레드 종료
                
                print("Stopping all motors due to obstacle detection.")
                motor_controller._stop()
                servo_kit.servo[0].angle = SERVO_ANGLES['C']  # 서보 초기 위치
                
                '''
                # 실행할 스크립트 파일 목록
                scripts = [('sudo','python','/home/a204/SDL_Pi_biBeaconScanner/location4.py')]

                processes = []

                # 각 스크립트를 새로운 프로세스로 실행
                for script in scripts:
                    process = subprocess.Popen(script)
                    processes.append(process)

                # 모든 프로세스가 종료될 때까지 대기
                for process in processes:
                    process.wait()

                print("모든 스크립트 실행 완료")
                #json 읽어오기
                    now_data = json.load(file)
                '''


                # 장애물 위치 업데이트
                next_direction = path[current_direction_index + 1] if (current_direction_index + 1) < len(path) else "unknown"

                '''#시현용
                add_x,add_y = GRID_MAP[cdir]
                next_direction.append(now_data["x"] + add_x)
                next_direction.append(now_data["y"] + add_y)'''
                
                robot_data['info']['block_x'] = next_direction[0]    
                robot_data['info']['block_y'] = next_direction[1]
                 # JSON 파일로 저장하기
                with open('robot_data.json', 'w') as json_file:
                    json.dump(robot_data, json_file, indent=4)    

                return {
                    'status': 'obstacle_detected',
                    'current_direction': cdir,
                    'obstacle_location': next_direction,
                    'current_location': path[current_direction_index]
                }
            time.sleep(1)

        servo_thread.join()
        motor_thread.join()

        print("All tasks completed.")
        mqtt_client.loop_stop()  # MQTT 클라이언트 루프 종료
        mqtt_client.disconnect()  # MQTT 클라이언트 연결 종료
        print("All tasks completed.")
        return {'status': 'completed'}    
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return {'status': 'error', 'message': str(e)}
    '''finally:
        stop_event.set()
        stop_event.set()  # 종료 이벤트 설정
        print("System stopped.")
        mqtt_client.loop_stop()  # MQTT 클라이언트 루프 종료
        mqtt_client.disconnect()  # MQTT 클라이언트 연결 종료
        print("All tasks completed.")
        return {'status': 'completed'}'''
