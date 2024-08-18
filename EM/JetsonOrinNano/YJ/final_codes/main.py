import subprocess

# 실행할 스크립트 파일 목록
# 절대 경로로 작성해야 파일 실행 위치에 따른 오류 방지 가능
scripts = ['/home/orin/final_run/announcement.py', 
           '/home/orin/final_run/jetson_ultrasonic.py', 
           '/home/orin/final_run/video_recode.py']
processes = []

# 각 스크립트를 새로운 프로세스로 실행
for script in scripts:
    process = subprocess.Popen(['python', script])
    processes.append(process)

# 모든 프로세스가 종료될 때까지 대기
for process in processes:
    process.wait()

print("모든 스크립트 실행 완료")