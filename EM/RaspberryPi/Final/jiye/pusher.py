from gpiozero import Servo
from time import sleep
import json


# 서보 핀 설정
servoPin = 4
cnt = 110
maxi = 110
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

def save_guide_liquid_to_json(guide_liquid):  # 추가된 부분
    data = {'guide_liquid': guide_liquid}
    with open('/home/a204/jiye/servo_guide_liquid.json', 'w') as json_file:
        json.dump(int(guide_liquid), json_file)

if __name__ == "__main__":  
    while True:
        # JSON 파일 읽기
        with open('/home/a204/qdrive/real_test/robot_data.json', 'r', encoding='utf-8') as file3:
            data = json.load(file3)
            value_mission=data["info"]["mission"]
            if value_mission == 2:
                print("pusher end!")
                exit()
    # 서보 0도에 위치
        for i in range(10):
            setServoPos(0)
            sleep(1) # 1초 대기

            setServoPos(80)
            sleep(1)
            cnt -= 1
            
        if cnt > 0:
            guide_liquid = (cnt / maxi) * 100
            print(f"Guide Liquid: {guide_liquid:.2f}%")
            save_guide_liquid_to_json(guide_liquid)  # JSON 파일에 guide_liquid 저장하는 부분 추가
    # 서보 중립 위치로 설정
    servo.value = 0
