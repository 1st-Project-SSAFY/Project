import json
from main_clean_code import run_a_star
import grid
from Drive_test_log import go_drive

# 상수 정의
INIT_PATH = 'init_path.json'
PATH_FILE = 'path.json'
DIRECTIONS_FILE = 'directions.json'
BROKER_ADDRESS = "3.36.55.201"
BROKER_PORT = 1883
TOPIC = "818/10F/escape-root"


def load_json(file_path):
    """JSON 파일에서 데이터를 로드합니다."""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    """데이터를 JSON 파일로 저장합니다."""
    with open(file_path, 'w') as file:
        json.dump(data, file)

# 방향 체크 상수
FORWARD_CONDITIONS = {
    'N': ['W', 'E', 'H', 'J'],
    'S': ['E', 'W', 'X', 'Z'],
    'E': ['N', 'S', 'J', 'X'],
    'W': ['S', 'N', 'H', 'Z'],
    'H': ['N', 'J', 'W', 'Z'],
    'J': ['E', 'X', 'N', 'H'],
    'Z': ['S', 'H', 'W', 'X'],
    'X': ['J', 'Z', 'E', 'S']
}

def is_backward(current_direction, target_direction):
    """현재 방향에서 지정된 방향으로 가는 것이 뒤로 가는 것인지 여부를 확인합니다."""
    return 1 if target_direction not in FORWARD_CONDITIONS.get(current_direction, []) else 0

def main():
    grid.create_and_save_grid(INIT_PATH)  # 초기 그리드를 생성하고 저장합니다.

    initial_direction = 'S'  # 초기 방향 설정
    start_position = grid.start  # 시작 위치 설정

    
    path_result = run_a_star(INIT_PATH, start_position, grid.goal)

    if path_result is None:
        print("Path not found")
        print("목표에 도달하지 못했습니다. 구조대를 호출합니다...")
        print("구조대 호출 완료!")

    # JSON 파일에서 데이터 로드
    path_data = load_json(PATH_FILE)
    directions_data = load_json(DIRECTIONS_FILE)

    backward = is_backward(initial_direction,directions_data['directions'][0])

    if backward==0: print("0")
    else : print("1")
    
    #if backward: print("good")

    # JSON 데이터 출력
    print("Loaded path from JSON:")
    print(path_data["path"])
    print("\nLoaded directions from JSON:")
    print(directions_data["directions"])

    # 로봇을 운전합니다.
    result = go_drive(initial_direction, backward)

        

if __name__ == "__main__":
    main()
