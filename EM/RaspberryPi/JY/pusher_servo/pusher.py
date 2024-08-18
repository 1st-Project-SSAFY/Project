from gpiozero import Servo
from time import sleep

# 서보 핀 설정
servoPin = 18

# Servo 객체 생성, gpiozero의 Servo는 -1에서 1까지 값을 사용 (0은 중앙)
servo = Servo(servoPin)

def setServoPos(degree):
    # 각도는 180도를 넘을 수 없다.
    if degree > 180:
        degree = 180

    # 각도(degree)를 -1에서 1 사이의 값으로 변경한다.
    position = (degree / 180.0) * 2 - 1
    # 위치 값 출력
    print(f"Degree: {degree} to {position}(Position)")

    # 변경된 위치 값을 서보에 적용
    servo.value = position

if __name__ == "__main__":  
    # 서보 0도에 위치
    setServoPos(0)
    sleep(1) # 1초 대기
    # 90도에 위치
    setServoPos(90)
    sleep(1)
    # 50도..
    setServoPos(50)
    sleep(1)

    # 120도..
    setServoPos(120)
    sleep(1)

    # 180도에 위치
    setServoPos(180)
    sleep(1)

    # 서보 중립 위치로 설정
    servo.value = None
