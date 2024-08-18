from adafruit_servokit import ServoKit
import time
import smbus2
import busio
import board

# I2C 버스 설정 (SCL 및 SDA 핀을 사용하여 I2C 버스 초기화)
i2c_bus = busio.I2C(board.D1, board.D0)

def i2c_scan(i2c):
    """
    I2C 버스를 스캔하여 연결된 모든 I2C 장치의 주소를 반환합니다.
    """
    while not i2c.try_lock():
        pass
    try:
        devices = i2c.scan()
        return devices
    finally:
        i2c.unlock()

try:
    print("Scanning I2C bus...")
    # I2C 버스를 스캔하여 연결된 장치 목록을 가져옴
    devices = i2c_scan(i2c_bus)
    print(f"I2C devices found: {[hex(device) for device in devices]}")

    if not devices:
        raise ValueError("No I2C devices found on the bus.")

    # PCA9685 PWM 드라이버 초기화 (서보 모터 제어를 위해 사용)
    try:
        kit = ServoKit(channels=16, i2c=i2c_bus, address=0x60)
        print("PCA9685 initialized at address 0x60.")
    except Exception as e:
        print(f"Error initializing PCA9685: {e}")
        raise

    # 서보 모터 초기 위치 설정
    pan = 0
    kit.servo[0].angle = pan

    print("Servo motors initialized.")
    print("Starting servo control test...")

    # 서보 모터 제어 테스트
    
    '''for i in range(0, 180):
        kit.servo[0].angle = i
        print(f"Servo 0 angle: {i}")
        time.sleep(0.05)  # 서보 모터의 각도 변경 후 잠시 대기
    for i in range(180, 0, -1):
        kit.servo[0].angle = i
        print(f"Servo 0 angle: {i}")
        time.sleep(0.05)  # 서보 모터의 각도 변경 후 잠시 대기
    #kit.servo[0].angle = 90
    #time.sleep(0.05)'''
    kit.servo[0].angle = 122


    print("Servo control test completed.")

except Exception as e:
    print(f"An error occurred: {e}")
