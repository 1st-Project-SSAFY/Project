import time
import Jetson.GPIO as GPIO
import paho.mqtt.client as mqtt

# MQTT 브로커 주소
broker_address = "3.36.55.201"

# MQTT 클라이언트 생성
Jetson = mqtt.Client()

# 주행 방향
selectedUltrasonic = "backward"
stopFlag = "notStart"

# MQTT 토픽 구독
def on_connect(client, data, flags, rc):
    print("초음파: 라즈베리파이 연결 성공")
    client.subscribe("ultrasonic/select")
    client.subscribe("destination/arrive/")
    
# MQTT 메시지가 들어온 경우 읽어오는 함수
def on_message(client, userdata, msg):
    global selectedUltrasonic, stopFlag
    topic = msg.topic
    if topic == "destination/arrive/":
        stopFlag = ""
        stopFlag = msg.payload.decode("utf-8")
        print(f"초음파: {stopFlag}")
    elif topic == "ultrasonic/select":
        selectedUltrasonic = msg.payload.decode("utf-8")

Jetson.on_connect = on_connect
Jetson.on_message = on_message
Jetson.connect(broker_address, 1883) # MQTT 브로커 연결
Jetson.loop_start()

# 앞으로 주행할 때 사용할 초음파
# 트리거 핀을 보드 15번, 에코 핀을 보드 7번에 연결
# GPIO 핀 번호와 다름, 보드 자체의 핀 번호
FORWARD_GPIO_TRIGGER = 15
FORWARD_GPIO_ECHO = 7

# 뒤로 주행할 때 사용할 초음파
# 트리거 핀을 보드 33번, 에코 핀을 보드 31번에 연결
# GPIO 핀 번호와 다름, 보드 자체의 핀 번호
BACKWARD_GPIO_TRIGGER = 33
BACKWARD_GPIO_ECHO = 31

GPIO.setmode(GPIO.BOARD)
 
# 초음파를 내보낼 트리거 핀은 출력 모드로, 반사파를 수신할 에코 핀은 입력모드로 설정
GPIO.setup(FORWARD_GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(BACKWARD_GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(FORWARD_GPIO_ECHO,GPIO.IN)
GPIO.setup(BACKWARD_GPIO_ECHO,GPIO.IN)

prev_direction = "forward"
 
try:
    while True:
        # 초음파 거리 측정에 사용할 변수
        stop = 0
        start = 0
        # print(selectedUltrasonic)
        
        # 앞으로 주행할 때
        if selectedUltrasonic == "forward":
            # 트리거 핀을 OFF 상태로 유지
            GPIO.output(FORWARD_GPIO_TRIGGER, False)
            time.sleep(0.5)
            
            # 10us 펄스를 내보냄
            # 파이썬에서 이 펄스는 실제 100us 근처가 될 것이지만, HC-SR04 센서에서 오차를 받아줌
            GPIO.output(FORWARD_GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(FORWARD_GPIO_TRIGGER, False)
            
            # 에코 핀이 ON되는 시점을 시작 시간으로 설정
            while GPIO.input(FORWARD_GPIO_ECHO)==0:
                start = time.time()
    
            # 에코 핀이 OFF되는 시점을 반사파 수신 시간으로 설정
            while GPIO.input(FORWARD_GPIO_ECHO)==1:
                stop = time.time()
        
        # 뒤로 주행할 때
        elif selectedUltrasonic == "backward":
            # 트리거 핀을 OFF 상태로 유지
            GPIO.output(BACKWARD_GPIO_TRIGGER, False)
            time.sleep(0.5)
            
            # 10us 펄스를 내보냄
            # 파이썬에서 이 펄스는 실제 100us 근처가 될 것이지만, HC-SR04 센서에서 오차를 받아줌
            GPIO.output(BACKWARD_GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(BACKWARD_GPIO_TRIGGER, False)
            
            # 에코 핀이 ON되는 시점을 시작 시간으로 설정
            while GPIO.input(BACKWARD_GPIO_ECHO)==0:
                start = time.time()

            # 에코 핀이 OFF되는 시점을 반사파 수신 시간으로 설정
            while GPIO.input(BACKWARD_GPIO_ECHO)==1:
                stop = time.time()
                
        # 초음파 길이 계산
        elapsed = stop-start
 
        if (stop and start):
            # 초음파는 반사파이기 때문에 초음파 길이 = 실제 이동 거리 * 2
            # 음속은 편의상 340m/s로 계산
            distance = (elapsed * 34000.0) / 2
            print("Distance : %.1f cm" % distance)
            print(f"prev_d: {prev_direction}, selectedD: {selectedUltrasonic}")
            print("")
            
            # 장애물까지의 거리가 80cm 이하일 때 라즈베리파이로 MQTT를 이용해 장애물이 감지되었음을 보냄
            # 장애물 검출 성공 후 여러 번 MQTT publish하는 것 방지
            if distance <= 70 and selectedUltrasonic != prev_direction:
                Jetson.publish("ultrasonic/detect/object", str(1))
                prev_direction = selectedUltrasonic
            else:
                Jetson.publish("ultrasonic/detect/object", str(0))
        print(selectedUltrasonic)
        # 너무 빠르게 검출될 경우 방지
        if stopFlag == "stop":
            print("초음파 종료")
            GPIO.cleanup()
            exit(0)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
