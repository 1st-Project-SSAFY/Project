from __future__ import print_function
# test BLE Scanning software
# SwitchDoc Labs December 2020 

import blescan
import sys
import bluetooth._bluetooth as bluez

# 특정 major value를 설정합니다.
target_major_value = "60"  # 원하는 major value로 변경하세요

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print("ble thread started")

except:
    print("error accessing bluetooth device...")
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
    returnedList = blescan.parse_events(sock, 10)
    print("----------")
    for beacon in returnedList:
        # 비콘 데이터에서 major value를 추출합니다.
        # blescan 모듈에서 parse_events 함수의 반환 형식에 따라 데이터 추출 방식이 다를 수 있습니다.
        # 일반적으로 major value는 비콘 데이터의 특정 위치에 있습니다.
        # 예를 들어, iBeacon 형식에서는 major value가 20번째 바이트부터 2바이트 길이로 포함됩니다.
        
        # 여기서는 가정된 형식으로 major value를 추출하는 예시를 보입니다.
        # 실제 형식에 맞게 수정해야 합니다.
        major_value = beacon.split(",")[2]
        
        if major_value == target_major_value:
            print(beacon)
        #print(major_value)
