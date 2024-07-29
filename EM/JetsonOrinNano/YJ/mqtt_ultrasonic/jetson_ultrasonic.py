import time
import Jetson.GPIO as GPIO
import paho.mqtt.client as mqtt

broker_address = "3.36.55.201"
Jetson = mqtt.Client("Jetson")
Jetson.connect(broker_address, 1883)
 
#핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BOARD)
 
# HC-SR04의 트리거 핀을 GPIO 17번, 에코핀을 GPIO 27번에 연결한다.
GPIO_TRIGGER = 7
GPIO_ECHO = 15
 
# 초음파를 내보낼 트리거 핀은 출력 모드로, 반사파를 수신할 에코 피은 입력 모드로 설정한다.
GPIO.setup(GPIO_TRIGGER,GPIO.OUT) 
GPIO.setup(GPIO_ECHO,GPIO.IN)
 
try:
    while True:
        stop = 0
        start = 0
        # 먼저 트리거 핀을 OFF 상태로 유지한다
        GPIO.output(GPIO_TRIGGER, False)
        time.sleep(2)
 
        # 10us 펄스를 내보낸다. 
        # 파이썬에서 이 펄스는 실제 100us 근처가 될 것이다.
        # 하지만 HC-SR04 센서는 이 오차를 받아준다.
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
 
        # 에코 핀이 ON되는 시점을 시작 시간으로 잡는다.
        while GPIO.input(GPIO_ECHO)==0:
            start = time.time()
 
        # 에코 핀이 다시 OFF되는 시점을 반사파 수신 시간으로 잡는다.
        while GPIO.input(GPIO_ECHO)==1:
            stop = time.time()
 
        # Calculate pulse length
        elapsed = stop-start
 
        # 초음파는 반사파이기 때문에 실제 이동 거리는 2배이다. 따라서 2로 나눈다.
        # 음속은 편의상 340m/s로 계산한다. 현재 온도를 반영해서 보정할 수 있다.
        if (stop and start):
            distance = (elapsed * 34000.0) / 2
            print("Distance : %.1f cm" % distance)
            if distance <= 60:
                Jetson.publish("ultrasonic/detect/object", 1)
            else:
                Jetson.publish("ultrasonic/detect/object", 0)
                
except KeyboardInterrupt:
    GPIO.cleanup()
 
 
# Reset GPIO settings
GPIO.cleanup()