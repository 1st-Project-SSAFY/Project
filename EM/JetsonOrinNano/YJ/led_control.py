import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
ch = [29, 31, 33, 32]

for channel in ch:
    GPIO.setup(channel, GPIO.OUT)
    
print("LED 시작")

while True:
    for channel in ch:
        GPIO.output(channel, GPIO.HIGH)
    time.sleep(0.3)
    for channel in ch:
        GPIO.output(channel, GPIO.LOW)
    time.sleep(0.3)
GPIO.cleanup()
