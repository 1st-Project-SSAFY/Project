# iBeacon과 삼변측량 기법을 활용한 실시간 실내 위치 측정 

- **iPhone의 Beacon Simulator app을 활용하여 iBeacon 대체**  
-> 안드로이드의 경우 AltBeacon으로 잡혀 활용하기 어려움  
-> 위치, 블루투스 허용 

- **testblesacn.py**: 근처 ble 장치 출력/ Mac adress-uuid-major-minor-tx power-rssi 순으로 출력/ *find_beacon_major.py or location.py 작동 안될 시 이 코드 먼저 실행 후 재시도*

- **find_beacon_major.py**: 특정 major 값을 가진 비콘만 출력

- **kalmantest.py**: rssi의 값에 kalman filter를 적용하여 rssi값의 오차를 줄임

- **location.py**: 최종코드, 찾을 특정 iBeacon의 major && minor 값을 입력하고 iBeacon들의 고정 좌표를 입력하여 코드를 실행하고 있는 장치의 위치를 좌표값으로 출력


## bluez 설치 필수 

- BLE 사용 시 설치 필수 


### bluez 설치 가이드

- [bluez 설치 가이드(in RaspberryPi5)](https://www.notion.so/Bluez-in-RaspberryPi5-ae3dc1f2341c44a4ab84504a474d3f9c)



