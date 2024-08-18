from playsound3 import playsound
import time
import paho.mqtt.client as mqtt

# MQTT 브로커 주소
broker_address = "3.36.55.201"

# MQTT 클라이언트 생성
Jetson = mqtt.Client()
stopFlag = "notStart"

# MQTT 토픽 구독
def on_connect(client, data, flags, rc):
    global stopFlag
    print("음성: 라즈베리파이 연결 성공")
    client.subscribe("destination/arrive/")
    
# MQTT 메시지가 들어온 경우 읽어오는 함수
def on_message(client, userdata, msg):
    global stopFlag
    stopFlag = ""
    stopFlag = msg.payload.decode("utf-8")
    print(f"음성: {stopFlag}")

Jetson.on_connect = on_connect
Jetson.on_message = on_message
Jetson.connect(broker_address, 1883) # MQTT 브로커 연결
Jetson.loop_start()


def ps():
    # 화재 대피 안내 음성 파일이 끝날 때까지 해당 함수 진행됨
    playsound("/home/orin/fire.mp3")

# 일정 시간마다 화재 대피 안내 음성 출력
while True:
    if stopFlag == "stop":
        break
    while stopFlag == "start":
        print("sound start")
        ps()
        if stopFlag == "stop":
            print("안내 종료")
            exit(0)
        # 화재 대피 안내 음성이 끝난 후 일정 시간 대기
        time.sleep(1)
    