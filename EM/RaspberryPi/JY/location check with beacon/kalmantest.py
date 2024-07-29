class KalmanFilter():
    def __init__(self, processNoise=0.005, measurementNoise=20):
        self.initialized = False
        self.processNoise = processNoise
        self.measurementNoise = measurementNoise
        self.predictedRSSI = 0
        self.errorCovariance = 0

    def filtering(self, rssi):
        if not self.initialized:
            self.initialized = True
            priorRSSI = rssi
            priorErrorCovariance = 1
        else:
            priorRSSI = self.predictedRSSI
            priorErrorCovariance = self.errorCovariance + self.processNoise

        kalmanGain = priorErrorCovariance / (priorErrorCovariance + self.measurementNoise)
        self.predictedRSSI = priorRSSI + (kalmanGain * (rssi - priorRSSI))
        self.errorCovariance = (1 - kalmanGain) * priorErrorCovariance

        return self.predictedRSSI

import blescan
import sys
import bluetooth._bluetooth as bluez

# 특정 major value를 설정합니다.
target_major_value = "60"  # 원하는 major value로 변경하세요

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print("BLE thread started")

except Exception as e:
    print(f"Error accessing Bluetooth device: {e}")
    sys.exit(1)

# KalmanFilter 인스턴스를 루프 밖에서 한 번만 생성합니다.
kf = KalmanFilter()

while True:
    returnedList = blescan.parse_events(sock, 10)
    for beacon in returnedList:
        # 비콘 데이터에서 major value를 추출합니다.
        major_value = beacon.split(",")[2]
        target_rssi = int(beacon.split(",")[5])  # target_rssi 값을 int로 변환

        if major_value == target_major_value:
            # RSSI 값을 필터링
            filtered_rssi = kf.filtering(target_rssi)
            
            print(beacon)
            print("Filtered RSSI Values:", filtered_rssi)
            print("--------------------------------------")
