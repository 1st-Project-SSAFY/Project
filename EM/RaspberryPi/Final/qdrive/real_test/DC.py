from adafruit_motor import motor
from adafruit_pca9685 import PCA9685
import board
import busio
import time

class PWMThrottleHat:
    def __init__(self, pwm, channel):
        """
        PWMThrottleHat 클래스 초기화
        :param pwm: PCA9685 인스턴스
        :param channel: 제어할 채널 번호
        """
        self.pwm = pwm
        self.channel = channel
        self.pwm.frequency = 60  # 주파수 설정

    def set_throttle(self, throttle):
        """
        스로틀 값을 설정하여 모터 제어
        :param throttle: -1.0 (후진)에서 1.0 (전진) 사이의 값
        """
        pulse = int(0xFFFF * abs(throttle))  # 16비트 듀티 사이클 계산
       
        if throttle > 0:
            # 전진
            self.pwm.channels[self.channel + 5].duty_cycle = pulse
            self.pwm.channels[self.channel + 4].duty_cycle = 0
            self.pwm.channels[self.channel + 3].duty_cycle = 0xFFFF
        elif throttle < 0:
            # 후진
            self.pwm.channels[self.channel + 5].duty_cycle = pulse
            self.pwm.channels[self.channel + 4].duty_cycle = 0xFFFF
            self.pwm.channels[self.channel + 3].duty_cycle = 0
        else:
            # 정지
            self.pwm.channels[self.channel + 5].duty_cycle = 0
            self.pwm.channels[self.channel + 4].duty_cycle = 0
            self.pwm.channels[self.channel + 3].duty_cycle = 0

# I2C 버스 설정
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60  # PCA9685 주파수 설정

# PWMThrottleHat 인스턴스 생성
motor_hat = PWMThrottleHat(pca, channel=0)

try:
    while True:
        print("Motor stop")
        motor_hat.set_throttle(0)  # 정지
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    motor_hat.set_throttle(0)  # 모터 정지
    pca.deinit()  # PCA9685 정리
    print("Program stopped and motor stopped.")
    
