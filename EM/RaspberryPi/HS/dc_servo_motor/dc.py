from gpiozero import Motor, PWMOutputDevice
from time import sleep

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

# 제어 시작

# 앞으로 80프로 속도로
setMotor(motor1, pwmA, 80, FORWARD)
sleep(5)

# 뒤로 40프로 속도로
setMotor(motor1, pwmA, 40, BACKWARD)
sleep(5)

# 뒤로 100프로 속도로
setMotor(motor1, pwmA, 100, BACKWARD)
sleep(5)

# 정지 
setMotor(motor1, pwmA, 0, STOP)

# 종료
motor1.close()
pwmA.close()
