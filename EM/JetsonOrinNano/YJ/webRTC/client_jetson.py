import socket
import cv2
import torch
import numpy as np

model = torch.hub.load('../yolov5', 'custom', path='../test/final_img640_batch32_epochs20_yolov5m.pt' , source='local', force_reload=True)

UDP_IP = "192.168.137.137"
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    frame = np.frombuffer(frame, dtype=np.uint8).reshape(480, 640, 3)
    # frame = cv2.resize(frame, (480, 320), cv2.INTER_LINEAR)
    
    results = model(frame)

        # 결과를 프레임에 그리기
    for detection in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = detection
        label = results.names[int(cls)]
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
        cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 3)
    # frame = cv2.resize(frame, (480, 640), cv2.INTER_LINEAR)
    
    d = frame.flatten()
    # s = d.tostring()
    s = d.tobytes()

    for i in range(20):
        sock.sendto(bytes([i]) + s[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
