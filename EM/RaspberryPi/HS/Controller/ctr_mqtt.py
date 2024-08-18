import pygame
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
import time
import threading
import paho.mqtt.client as mqtt

# I2C 버스 설정
i2c_0 = busio.I2C(board.D1, board.D0)
i2c_1 = busio.I2C(board.SCL, board.SDA)

# PCA9685 인스턴스 생성
pca_dc = PCA9685(i2c_1, address=0x40)
pca_dc.frequency = 60  # PCA9685 주파수 설정

# MQTT 클라이언트 설정
broker_address = "3.36.55.201"
mqtt_client = mqtt.Client("Pi")

def on_connect(client, userdata, flags, rc):
    """MQTT 브로커에 연결되었을 때 호출되는 콜백 함수"""
    print("Connected!")
    client.subscribe("ultrasonic/detect/object")

def on_message(client, userdata, msg):
    """MQTT 메시지를 수신했을 때 호출되는 콜백 함수"""
    if msg.topic == 'ultrasonic/detect/object' and msg.payload.decode() == '1':
        print("Obstacle detected!")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(broker_address, 1883)
mqtt_client.loop_start()

# 서보 모터 제어 설정
kit_servo = ServoKit(channels=16, i2c=i2c_0, address=0x60)

class PWMThrottleHat:
    """DC 모터 제어 클래스"""
    def __init__(self, pwm, channel):
        self.pwm = pwm
        self.channel = channel
        self.pwm.frequency = 60  # 주파수 설정

    def set_throttle(self, throttle):
        """모터의 스로틀을 설정합니다."""
        throttle = max(min(throttle, 1.0), -1.0)  # 스로틀 범위 조정
        pulse = int(0xFFFF * abs(throttle))  # 16비트 듀티 사이클 계산
        pulse = min(pulse, 0xFFFF)
        if throttle > 0:
            self._set_forward(pulse)
        elif throttle < 0:
            self._set_reverse(pulse)
        else:
            self._stop()

    def _set_forward(self, pulse):
        """전진 모드 설정"""
        self.pwm.channels[self.channel + 5].duty_cycle = pulse
        self.pwm.channels[self.channel + 4].duty_cycle = 0
        self.pwm.channels[self.channel + 3].duty_cycle = 0xFFFF

    def _set_reverse(self, pulse):
        """후진 모드 설정"""
        self.pwm.channels[self.channel + 5].duty_cycle = pulse
        self.pwm.channels[self.channel + 4].duty_cycle = 0xFFFF
        self.pwm.channels[self.channel + 3].duty_cycle = 0

    def _stop(self):
        """모터 정지"""
        self.pwm.channels[self.channel + 5].duty_cycle = 0
        self.pwm.channels[self.channel + 4].duty_cycle = 0
        self.pwm.channels[self.channel + 3].duty_cycle = 0

# DC 모터 인스턴스 생성
motor_hat = PWMThrottleHat(pca_dc, channel=0)

# Pygame 초기화 및 Xbox 컨트롤러 설정
pygame.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()

# 서보 모터 제어 변수
current_pan = 120
target_pan = current_pan
servo_lock = threading.Lock()

def move_servo_smoothly(kit, channel, current_angle, target_angle, step=1, delay=0.01):
    """서보 모터를 부드럽게 이동시킵니다."""
    with servo_lock:
        current_angle = int(current_angle)
        target_angle = int(target_angle)
        step = abs(step)
        angle_range = range(current_angle, target_angle + 1, step) if current_angle < target_angle else range(current_angle, target_angle - 1, -step)
        for angle in angle_range:
            kit.servo[channel].angle = angle
            time.sleep(delay)

def handle_servo():
    """서보 모터 제어 스레드"""
    global current_pan, target_pan
    while True:
        if current_pan != target_pan:
            move_servo_smoothly(kit_servo, 0, current_pan, target_pan)
            current_pan = target_pan
        time.sleep(0.1)

def handle_controller():
    """Xbox 컨트롤러 입력 처리 스레드"""
    global target_pan
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYHATMOTION:
                    if event.hat == 0:  # 방향키 입력
                        if event.value[0] == 1:
                            target_pan += 10
                        elif event.value[0] == -1:
                            target_pan -= 10
                        target_pan = max(min(target_pan, 180), 0)
                
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        motor_hat.set_throttle(1)  # 전진
                    elif event.button == 1:
                        motor_hat.set_throttle(-1)  # 후진
                    elif event.button == 2:
                        motor_hat.set_throttle(0)  # 정지
                    elif event.button == 3:
                        target_pan = 120
                        with servo_lock:
                            kit_servo.servo[0].angle = target_pan
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

# 서보 모터 및 컨트롤러 처리를 위한 스레드 생성
servo_thread = threading.Thread(target=handle_servo)
controller_thread = threading.Thread(target=handle_controller)

servo_thread.start()
controller_thread.start()

try:
    while True:
        time.sleep(1)
        print(f"Current Pan Angle: {current_pan} degrees")
except KeyboardInterrupt:
    pass
finally:
    motor_hat.set_throttle(0)  # 모터 정지
    kit_servo.servo[0].angle = 120  # 서보 모터 초기 위치로 리셋
    pca_dc.deinit()  # PCA9685 정리
    pygame.quit()  # Pygame 종료
    print("Program stopped and motor stopped.")
