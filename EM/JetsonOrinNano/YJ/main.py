import subprocess

# 실행할 스크립트 파일 목록
scripts = ['jetson_ultrasonic.py', 'LED_test.py', 'webRTC/client_jetson.py']

processes = []

# 각 스크립트를 새로운 프로세스로 실행
for script in scripts:
    process = subprocess.Popen(['python', script])
    processes.append(process)

# 모든 프로세스가 종료될 때까지 대기
for process in processes:
    process.wait()

print("모든 스크립트 실행 완료")
