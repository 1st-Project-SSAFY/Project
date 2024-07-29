import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# 모델 파일 경로 설정
model_path = 'train_fire.h5'
label_path = 'labels.txt'

# Keras 모델 로드
model = load_model(model_path)

# 모델의 입력 크기 및 형식 확인
input_shape = model.layers[0].input_shape[1:4]
print(f"Expected input shape: {input_shape}")

# Load the labels
def load_labels(label_path):
    with open(label_path, 'r') as f:
        labels = f.read().splitlines()
    return {i: label for i, label in enumerate(labels)}

labels = load_labels(label_path)

def preprocess_image(image, input_shape):
    image = cv2.resize(image, (input_shape[1], input_shape[0]))  # 모델에 맞는 입력 크기로 조정
    if input_shape[2] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 흑백 이미지로 변환
    image = image / 255.0  # 정규화
    image = np.expand_dims(image, axis=-1) if input_shape[2] == 1 else image
    image = np.expand_dims(image, axis=0)
    return image

def detect_objects(image, model, input_shape, threshold=0.5):
    preprocessed_image = preprocess_image(image, input_shape)
    predictions = model.predict(preprocessed_image)
    detections = []
    for i, score in enumerate(predictions[0]):
        if score > threshold:
            detections.append((i, score))
    return detections

# Initialize webcam
cap = cv2.VideoCapture(0)

# 트래커 초기화
tracker = cv2.TrackerCSRT_create()

# 첫 번째 프레임에서 객체 검출
ret, frame = cap.read()
detections = detect_objects(frame, model, input_shape)

# 첫 번째 객체의 위치로 트래커 초기화
if detections:
    bbox = cv2.selectROI('Object Detection', frame, fromCenter=False, showCrosshair=True)
    tracker.init(frame, bbox)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 객체 검출 및 트래킹
    success, bbox = tracker.update(frame)
    if success:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
    else:
        # 객체가 트래킹되지 않으면 다시 검출
        detections = detect_objects(frame, model, input_shape)
        if detections:
            bbox = cv2.selectROI('Object Detection', frame, fromCenter=False, showCrosshair=True)
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, bbox)

    # 프레임 표시
    cv2.imshow('Object Detection & Tracking', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
