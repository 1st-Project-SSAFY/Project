import json
from main import run_a_star  # main 모듈에서 run_a_star 함수 import
import grid  # grid 모듈 import
from mtr_ctr_for_mqtt import go_drive
import paho.mqtt.client as mqtt

init_path = 'init_path.json'  # 초기화할 그리드 파일 경로

def load_json(file_path):
    """
    JSON 파일을 로드하는 함수
    
    Args:
    - file_path: JSON 파일 경로
    
    Returns:
    - JSON 데이터
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path, data):
    """
    데이터를 JSON 파일로 저장하는 함수
    
    Args:
    - file_path: JSON 파일 경로
    - data: 저장할 데이터
    """
    with open(file_path, 'w') as f:
        json.dump(data, f)

def check_backward(cur_dir,go_dir):
    if cur_dir == 'N':
        if go_dir != 'W' and go_dir != 'E' and go_dir != 'H' and go_dir != 'J':
            return 1 #뒤로 가야함
        else:
            return 0 #앞으로 가도됨
    elif cur_dir == 'S':
        if go_dir != 'E' and go_dir != 'W' and go_dir != 'X' and go_dir != 'Z':
            return 1
        else:
            return 0
    elif cur_dir == 'E':
        if go_dir != 'N' and go_dir != 'S' and go_dir != 'J' and go_dir != 'X':
            return 1
        else:
            return 0
    elif cur_dir == 'W':
        if go_dir != 'S' and go_dir != 'N' and go_dir != 'H' and go_dir != 'Z':
            return 1
        else:
            return 0
    elif cur_dir == 'H':
        if go_dir != 'N' and go_dir != 'J' and go_dir != 'W' and go_dir != 'Z':
            return 1
        else:
            return 0
    elif cur_dir == 'J':
        if go_dir != 'E' and go_dir != 'X' and go_dir != 'N' and go_dir != 'H':
            return 1
        else:
            return 0
    elif cur_dir == 'Z':
        if go_dir != 'S' and go_dir != 'H' and go_dir != 'W' and go_dir != 'X':
            return 1
        else:
            return 0
    elif cur_dir == 'X':
        if go_dir != 'J' and go_dir != 'Z' and go_dir != 'E' and go_dir != 'S':
            return 1
        else:
            return 0

def main():
    grid.create_and_save_grid(init_path)  # 초기 그리드 생성 및 저장
    broker_address = "3.36.55.201"
    pi = mqtt.Client("Pi")
    pi_dir = 'S'
    start = grid.start
    while True:
        # A* 알고리즘 실행 및 경로 확인
        if run_a_star(init_path, start, grid.goal) is None:
            print("Can't find path")
            print("Failed to reach the destination. Calling the rescue team...")
            print("Rescue team called!")
            break    

        pi.connect(broker_address,1883)
        with open("path.json",'rb') as f:
            file_data = f.read()

        pi.publish("pi/expected_path",file_data)        
        pi.loop_forever()

        # JSON 파일 불러오기
        path_data = load_json("path.json")
        directions_data = load_json("directions.json")

        bckwrd = check_backward(pi_dir,directions_data[0])

        # JSON 데이터 출력
        print("Loaded path from JSON:")
        print(path_data["path"])
        print("\nLoaded directions from JSON:")
        print(directions_data["directions"])

        result = go_drive(pi_dir,bckwrd)

        if result['status'] == 'obstacle_detected':
            print(f"Obstacle detected at location: {result['obstacle_location']}")

            # 그리드 업데이트
            grid_data = load_json(init_path)
            obstacle_location = result['obstacle_location']
            if obstacle_location != "unknown":
                x, y = obstacle_location  # 장애물 위치 좌표
                grid_data[x][y] = 1  # 장애물을 1로 표시

                # 그리드 저장
                save_json(init_path, grid_data)
                print("Grid updated with new obstacle location.")
                pi_dir = result['current_direction']
                start = result['current_location']

        elif result['status'] == 'completed':
            print("Destination reached successfully!")
            break

        elif result['status'] == 'error':
            print(f"An error occurred: {result['message']}")
            break

if __name__ == "__main__":
    main()
