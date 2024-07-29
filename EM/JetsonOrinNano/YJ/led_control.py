import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
ch = [29, 31, 33]

for channel in ch:
    GPIO.setup(channel, GPIO.OUT)

while True:
    for channel in ch:
        GPIO.output(channel, GPIO.HIGH)
    time.sleep(0.7)
    for channel in ch:
        GPIO.output(channel, GPIO.LOW)
    time.sleep(0.7)
GPIO.cleanup()
