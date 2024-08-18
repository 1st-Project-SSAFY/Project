import board
import busio
from gpiozero import LED
from adafruit_bus_device.i2c_device import I2CDevice
import time

# I2C 버스 설정
i2c = busio.I2C(board.SCL, board.SDA)

# Maxim IC 주소 (문서에서 확인된 주소를 사용하세요)
MAXIM_ADDRESS = 0x36
device = I2CDevice(i2c, MAXIM_ADDRESS)

# LED 핀 설정
led_pins = [5, 12, 13, 19]
leds = [LED(pin) for pin in led_pins]

def read_battery_data():
    try:
        # 배터리 전압 및 상태를 읽기 위한 레지스터 주소 (문서에서 확인)
        REG_BATTERY_VOLTAGE = 0x00

        # 레지스터에서 데이터 읽기
        buffer = bytearray(2)
        with device:
            device.write_then_readinto(bytearray([REG_BATTERY_VOLTAGE]), buffer)
        voltage = (buffer[0] << 8) | buffer[1]

        # 배터리 전압 계산 (단위는 mV로 변환)
        battery_voltage = voltage * 0.1  # 변환 비율은 데이터시트에서 확인

        # 배터리 잔량 계산 (0%에서 100% 사이)
        min_voltage = 3000  # 최소 전압 (3.0V)
        max_voltage = 4200  # 최대 전압 (4.2V)
        battery_percentage = (battery_voltage - min_voltage) / (max_voltage - min_voltage) * 100
        battery_percentage = max(0, min(100, battery_percentage))  # 0% ~ 100% 사이로 제한

        print(f"Battery Voltage: {battery_voltage:.2f} mV")
        print(f"Battery Percentage: {battery_percentage:.2f}%")

        return battery_percentage

    except Exception as e:
        print(f"Error reading battery data: {e}")
        return None

def leds_on(count):
    for i, led in enumerate(leds):
        if i < count:
            led.on()
        else:
            led.off()

# 메인 루프
try:
    while True:
        battery_percentage = read_battery_data()
        if battery_percentage is not None:
            # 배터리 잔량에 따라 LED 제어
            if battery_percentage >= 75:
                leds_on(4)
            elif battery_percentage >= 50:
                leds_on(3)
            elif battery_percentage >= 25:
                leds_on(2)
            elif battery_percentage >= 5:
                leds_on(1)
            else:
                leds_on(0)

        time.sleep(10)  # 10초마다 배터리 상태 확인

except KeyboardInterrupt:
    print("프로그램 종료")

finally:
    for led in leds:
        led.off()  # 프로그램 종료 시 모든 LED 끄기
