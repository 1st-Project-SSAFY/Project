import socket
import numpy
import cv2

# 소켓 통신할 IP랑 포트
UDP_IP = "70.12.246.98"
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# 버퍼 초기화
# 해당 버퍼는 나중에 이미지 데이터를 임시로 저장할 때 사용
s = [b'\xff' * 46080 for x in range(20)]

# 비디오 코덱 설정
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# output.avi 파일로 비디오 파일 초기화
# 프레임 속도 10 fps, 해상도 640*480
# 저장된 영상 속도가 빠른 경우 프레임 속도를 낮출 것
out = cv2.VideoWriter('output.avi', fourcc, 10.0, (640, 480))

while True:
    picture = b''

    # UDP 소켓으로부터 46081 바이트 크기의 데이터 수신
    # 수신 데이터의 첫 바이트는 데이터 블록의 인덱스
    # 나머지 46080 바이트는 실제 이미지 데이터
    data, addr = sock.recvfrom(46081)
    s[data[0]] = data[1:46081]

    # 인덱스가 19인 경우(== 마지막 데이터 블록이 수신된 경우) 20개의 데이터 블록을 모두 결합하여 하나의 전체 이미지 생성
    if data[0] == 19:
        for i in range(20):
            picture += s[i]

        frame = numpy.fromstring(picture, dtype=numpy.uint8)
        frame = frame.reshape(480, 640, 3)
        cv2.imshow("frame", frame)
        # 비디오 파일에 저장
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break