import json
import paho.mqtt.client as mqtt
from main_clean_code import run_a_star
import grid
from Drive_test_log import go_drive
import time

# 상수 정의
INIT_PATH = '/home/a204/qdrive/real_test/init_path.json'
PATH_FILE = '/home/a204/qdrive/real_test/path.json'
PATH_COPY_FILE = '/home/a204/qdrive/real_test/path_copy.json'
DIRECTIONS_FILE = '/home/a204/qdrive/real_test/directions.json'
BROKER_ADDRESS = "3.36.55.201"
BROKER_PORT = 1883
TOPIC = "escape-root/818/10/"

# 방향 체크 상수
FORWARD_CONDITIONS = {
    'N': ['W', 'E', 'H', 'J','N'],
    'S': ['E', 'W', 'X', 'Z','S'],
    'E': ['N', 'S', 'J', 'X','E'],
    'W': ['S', 'N', 'H', 'Z','W'],
    'H': ['N', 'J', 'W', 'Z','H'],
    
    'J': ['E', 'X', 'N', 'H','J'],
    'Z': ['S', 'H', 'W', 'X','Z'],
    'X': ['J', 'Z', 'E', 'S','X']
}

def load_json(file_path):
    """JSON 파일에서 데이터를 로드합니다."""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    """데이터를 JSON 파일로 저장합니다."""
    with open(file_path, 'w') as file:
        json.dump(data, file)

def is_backward(current_direction, target_direction):
    """현재 방향에서 지정된 방향으로 가는 것이 뒤로 가는 것인지 여부를 확인합니다."""
    return 1 if target_direction not in FORWARD_CONDITIONS.get(current_direction, []) else 0

def setup_mqtt_client():
    """MQTT 클라이언트를 설정하고 반환합니다."""
    client = mqtt.Client("robot")
    client.connect(BROKER_ADDRESS, BROKER_PORT)
    return client

def publish_json_data(client, topic, file_path):
    """JSON 파일의 데이터를 MQTT 주제로 퍼블리시합니다."""
    data = load_json(file_path)
    client.publish(topic, json.dumps(data))
    print("====================PUB======================")

def on_connect(client, userdata, flags, rc):
    """MQTT 브로커에 연결되었을 때 호출되는 콜백 함수입니다."""
    print("Connected!")
    client.subscribe(TOPIC)

def main():
    grid.create_and_save_grid(INIT_PATH)  # 초기 그리드를 생성하고 저장합니다.

    mqtt_client = setup_mqtt_client()
    mqtt_client.on_connect = on_connect
    mqtt_client.loop_start()  # MQTT 클라이언트의 메시지 루프를 시작합니다.

    initial_direction = 'W'  # 초기 방향 설정
    start_position = grid.start  # 시작 위치 설정
    Motor_toggle = 'f'

    while True:
        # A* 알고리즘을 실행하여 경로를 찾습니다.
        path_result = run_a_star(INIT_PATH, start_position, grid.goal)

        if path_result is None:
            print("Path not found")
            #목표지점까지 가지 못하게 될 때 publish
            mqtt_client.publish("robot/mission/result","fail")
            print("목표에 도달하지 못했습니다. 구조대를 호출합니다...")
            print("구조대 호출 완료!")
            break

        # JSON 파일에서 데이터 로드
        path_data = load_json(PATH_FILE)
        directions_data = load_json(DIRECTIONS_FILE)

        print(f"Initial Direction: {initial_direction}, Target Direction:{directions_data['directions'][0]}")

        # 로봇의 방향과 목표 방향 계산
        backward = 1
        if Motor_toggle == 'f':
            if is_backward(initial_direction, directions_data['directions'][0]) == 1:
                backward = 1
                Motor_toggle = 'b'
            else:
                backward = 0
        elif Motor_toggle == 'b':
            if is_backward(initial_direction, directions_data['directions'][0]) == 1:
                backward = 0
                Motor_toggle = 'f'
            else:
                backward = 1

        # JSON 데이터 퍼블리시: 경로와 방향을 MQTT로 전송
        if load_json(PATH_COPY_FILE) != {}:
            publish_json_data(mqtt_client, TOPIC, PATH_COPY_FILE)
            save_json(PATH_COPY_FILE, {})

        # JSON 데이터 출력
        print("Loaded path from JSON:")
        print(path_data["path"])
        print("\nLoaded directions from JSON:")
        print(directions_data["directions"])

        # 로봇을 운전합니다.
        time.sleep(5)
        result = go_drive(initial_direction, backward)

        if result['status'] == 'obstacle_detected':
            print(f"장애물이 위치한 곳: {result['obstacle_location']}")
            print(f"현재 위치한 곳: {result['current_location']}")

            # 새로운 장애물로 그리드를 업데이트합니다.
            grid_data = load_json(INIT_PATH)
            obstacle_location = result['obstacle_location']
            if obstacle_location != "unknown":
                x, y = obstacle_location
                grid_data[x][y] = 1  # 장애물로 표시

                save_json(INIT_PATH, grid_data)
                print("새 장애물 위치로 그리드를 업데이트했습니다.")
                # 장애물이 탐지된 경우 데이터 퍼블리시
                # publish_json_data(mqtt_client, TOPIC, INIT_PATH)
                initial_direction = result['current_direction']
                print(f"Current Direction:{initial_direction}")
                start_position = tuple(result['current_location'])

        elif result['status'] == 'completed':
            print("목표에 성공적으로 도달했습니다!")
            # 목표에 도달한 경우 데이터 퍼블리시
            robot_data = load_json('robot_data.json')
            robot_data["info"]["mission"] = 2
            # JSON 파일로 저장하기
            with open('robot_data.json', 'w') as json_file:
                json.dump(robot_data, json_file, indent=4)
            #mqtt_client.publish("robot/mission/result",2)
            break

        elif result['status'] == 'error':
            print(f"오류가 발생했습니다: {result['message']}")
            # 오류가 발생한 경우 데이터 퍼블리시
            break

if __name__ == "__main__":
    time.sleep(8)
    main()
