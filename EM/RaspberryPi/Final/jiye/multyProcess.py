import subprocess
import signal
import paho.mqtt.client as mqtt
import json
import time

# 실행할 스크립트 파일 목록
scripts = [
    ('sudo','python','/home/a204/jiye/x120x/battery.py'), 
    ('python','/home/a204/jiye/mqtt_count.py')
    ]
processes = []

def on_connect1(client, userdata, flags, rc):
    print("workConnected!")
    client.subscribe("work_robot/")

robots_list = []

def on_message1(client, userdata, msg):
    global robots_list
    message = msg.payload.decode('utf-8')
    # Convert the JSON string to a Python list
    robots_list = json.loads(message)
    print(robots_list)
    
    # Check if 'ROBOT5632' is in the list
    if 'ROBOT5632' in robots_list:
        terminate_and_restart_processes()

def terminate_and_restart_processes():
    print("Terminating all processes...")
    for process in processes:
        process.terminate()  # 프로세스에 종료 신호 보내기
        process.wait()  # 프로세스가 완전히 종료될 때까지 대기

    processes.clear()  # 프로세스 리스트 비우기

    # MQTT 루프 정지
    #pi.loop_stop()
    #pi.disconnect()

    # work 프로세스 시작하기
    scripts_work = [
        ('python','/home/a204/qdrive/real_test/start_clean_code.py'),
        ('python', '/home/a204/jiye/pusher.py'), 
        ('sudo','python','/home/a204/jiye/x120x/battery.py'), 
        ('python','/home/a204/jiye/mqtt_work.py')
        ]
    processes_work = []

    # 각 스크립트를 새로운 프로세스로 실행
    for script_work in scripts_work:
        try:
            process_work = subprocess.Popen(script_work)
            processes_work.append(process_work)
        except Exception as e:
            print(f"Failed to start {script_work}: {e}")

    # 모든 프로세스가 종료될 때까지 대기
    for process_work in processes_work:
        process_work.wait()

    print("모든 스크립트 실행 완료")


# 각 스크립트를 새로운 프로세스로 실행
for script in scripts:
    try:
        process = subprocess.Popen( script)
        processes.append(process)
    except Exception as e:
        print(f"Failed to start {script}: {e}")

broker_address = "3.36.55.201"
work = mqtt.Client("work")
work.on_connect = on_connect1
work.on_message = on_message1

work.connect(broker_address, 1883)
work.loop_start()

try:
    # 메시지가 'ROBOT5632'일 경우 모든 프로세스를 종료
    while True:
        time.sleep(1)  # CPU 소모를 줄이기 위해 잠시 대기
except KeyboardInterrupt:
    print("Terminating script...")
    for process in processes:
        process.terminate()
        process.wait()
    work.loop_stop()
    work.disconnect()

print("MQTT client disconnected and all processes terminated.")

