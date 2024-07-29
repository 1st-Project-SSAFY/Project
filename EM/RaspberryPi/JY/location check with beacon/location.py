import blescan
import sys
import bluetooth._bluetooth as bluez
import time
import numpy as np

# 필요한 모듈과 클래스 정의 (예: KF, AP, Trilateration 등)
class KF:
    def __init__(self):
        # 칼만 필터 초기화
        pass

    def filtering(self, value):
        # 간단한 필터링 예제
        # 실제 필터링 로직을 구현해야 함
        return value

class AP:
    def __init__(self, x, y, distance):
        self.x = x
        self.y = y
        self.distance = distance

class Trilateration:
    def __init__(self, AP1, AP2, AP3):
        self.AP1 = AP1
        self.AP2 = AP2
        self.AP3 = AP3
    
    def calcUserLocation(self):
        A = 2 * (self.AP2.x - self.AP1.x)
        B = 2 * (self.AP2.y - self.AP1.y)
        C = self.AP1.distance**2 - self.AP2.distance**2 - self.AP1.x**2 + self.AP2.x**2 - self.AP1.y**2 + self.AP2.y**2
        D = 2 * (self.AP3.x - self.AP2.x)
        E = 2 * (self.AP3.y - self.AP2.y)
        F = self.AP2.distance**2 - self.AP3.distance**2 - self.AP2.x**2 + self.AP3.x**2 - self.AP2.y**2 + self.AP3.y**2
        
        user_x = ( (F * B) - (E * C) ) / ( (B * D) - (E * A))
        user_y = ( (F * A) - (D * C) ) / ( (A * E) - (D * B))
        return user_x, user_y


# 필터 객체 생성
kf = KF()

# Bluetooth 장치 초기화
dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print("Bluetooth device opened successfully")
except Exception as e:
    print("Error accessing Bluetooth device...", e)
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

# 비콘 데이터를 주기적으로 수신하여 위치를 계산하는 함수
def measure_and_calculate_location():
    while True:
        beacons = blescan.parse_events(sock, 10)
        #if not beacons:
        #    print("No beacons found")
        #else:
        #    print(f"Found {len(beacons)} beacons")
        
        # 초기화
        filtered_rssi1 = 0
        filtered_rssi2 = 0
        filtered_rssi3 = 0

        for beacon in beacons:
            #print(f"Processing beacon: {beacon}")
            # 예시: beacon 데이터가 "major_value,target_major_value,15,-65" 형태로 제공된다고 가정
            beacon_data = beacon.split(',')
            major_value = beacon_data[2]
            target_major_value = "60"
            minor_value = beacon_data[3]
            rssi_value = beacon_data[5]

            if major_value == target_major_value:
                if minor_value == "15":
                    target_rssi1 = int(rssi_value)
                    # RSSI 값을 필터링
                    filtered_rssi1 = kf.filtering(target_rssi1)
                if minor_value == "7":
                    target_rssi2 = int(rssi_value)
                    # RSSI 값을 필터링
                    filtered_rssi2 = kf.filtering(target_rssi2)
                if minor_value == "1":
                    target_rssi3 = int(rssi_value)
                    # RSSI 값을 필터링
                    filtered_rssi3 = kf.filtering(target_rssi3)

        if filtered_rssi1 != 0 or filtered_rssi2 != 0 or filtered_rssi3 != 0:
            print("Filtered RSSI1 Values:", filtered_rssi1)
            print("Filtered RSSI2 Values:", filtered_rssi2)
            print("Filtered RSSI3 Values:", filtered_rssi3)
            print("--------------------------------------")

            # AP 객체 생성
            ap1 = AP(4, 4, np.sqrt((-1)*filtered_rssi1))
            ap2 = AP(12, 4, np.sqrt((-1)*filtered_rssi2))
            ap3 = AP(8, 12, np.sqrt((-1)*filtered_rssi3))

            # 삼변측량 계산
            tril = Trilateration(ap1, ap2, ap3)
            x, y = tril.calcUserLocation()
            print(x)
            print(y)
            print("--------------------------------------")

        time.sleep(2)  # 2초 대기

# 측정 및 위치 계산 시작
measure_and_calculate_location()
