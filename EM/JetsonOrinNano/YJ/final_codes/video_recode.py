from cam_find import cam_find
import cv2
import torch
import numpy as np
import paho.mqtt.client as mqtt

# MQTT 브로커 주소
broker_address = "3.36.55.201"

# MQTT 클라이언트 생성
Jetson = mqtt.Client()

stopFlag = "notStart"

# MQTT 토픽 구독
def on_connect(client, data, flags, rc):
    print("비디오: 라즈베리파이 연결 성공")
    client.subscribe("destination/arrive/")
    
# MQTT 메시지가 들어온 경우 읽어오는 함수
def on_message(client, userdata, msg):
    global stopFlag
    stopFlag = ""
    stopFlag = msg.payload.decode("utf-8")
    print(f"비디오: {stopFlag}")

Jetson.on_connect = on_connect
Jetson.on_message = on_message
Jetson.connect(broker_address, 1883) # MQTT 브로커 연결
Jetson.loop_start()

# YOLOv5 학습 모델 불러오기
# 모델 확장자가 .pt인 경우 모델의 state_dict만 저장되어있음
# 즉 학습 가능한 매개변수(가중치, 편향)만 담겨있기 때문에 이미 구현되어 있는 모델을 로드해야 함
# 모델 확장자가 .pth인 경우 모델 전체가 저장되어있음
# 즉 모델의 parameter, optimizer, epoch, score 등의 모든 상태 저장 -> 추후 이어서 학습하거나 코드 접근 권한이 없는 사용자가 모델을 사용할 수 있음
model = torch.hub.load('/home/orin/yolov5', 'custom', path='/home/orin/test/final_model.pt' , source='local', force_reload=True)

# 현재 디바이스에 연결된 카메라 모듈을 전부 불러오는 함수
c1, c2 = cam_find()
cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(2)

# 이미지 크기를 640 * 480으로 설정
cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 카메라가 정상적으로 연결되었는지 확인
print(c1, c2)

# fourcc = DIVX (*는 문자를 풀어쓰는 방식, 즉 *'DIVX' == 'D', 'I', 'V', 'X')
# fps(frame per sec) = 30.0 -> 숫자가 높을 수록 영상이 빨라지는 경향이 있음
# 저장할 비디오의 화면 크기 = 1280 * 480
outputVideo = cv2.VideoWriter('/home/orin/final_run/Video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 20.0, (1280, 480))

try:
    while True:
        while stopFlag == "start":
            ret1, frame1 = cam1.read()
            ret2, frame2 = cam2.read()
            if stopFlag == "stop":
                print("비디오 종료")
                # 카메라 자원 할당 해제
                outputVideo.release()
                cam1.release()
                cam2.release()
                exit(0)
            
            if not ret1 and not ret2:
                break
            
            # 카메라에서 읽어온 프레임 크기를 640 * 480으로 조정
            frame1 = cv2.resize(frame1, (640, 480), cv2.INTER_LINEAR)
            frame2 = cv2.resize(frame2, (640, 480), cv2.INTER_LINEAR)
            
            # results1, results2는 프레임에서 학습 결과물이 검출되었는지에 대한 결과(detection 결과)
            results1 = model(frame1)
            results2 = model(frame2)
            
            # 예측 결과를 프레임에 그리기
            for detection in results1.xyxy[0]:
                x1, y1, x2, y2, conf, cls = detection
                label = results1.names[int(cls)]
                cv2.rectangle(frame1, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
                cv2.putText(frame1, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 3)
                
            for detection in results2.xyxy[0]:
                x1, y1, x2, y2, conf, cls = detection
                label = results2.names[int(cls)]
                cv2.rectangle(frame2, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
                cv2.putText(frame2, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 3)
            
            # frame1과 frame2를 가로 기준으로 합쳐서 하나의 프레임으로 만들기
            frame = cv2.hconcat([frame1, frame2])
            
            # 합친 프레임을 동영상으로 저장하기
            outputVideo.write(frame)
            
            # 'q' 키를 누르면 실행 종료
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
except KeyboardInterrupt:
    print("비디오 종료")
    # 카메라 자원 할당 해제
    outputVideo.release()
    cam1.release()
    cam2.release()