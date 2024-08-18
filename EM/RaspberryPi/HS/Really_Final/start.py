import json
from main import run_a_star  # main 모듈에서 run_a_star 함수 import
import grid  # grid 모듈 import
#from mtr_ctr import go_drive


init_path = 'init_path.json'  # 초기화할 그리드 파일 경로
my_direction = 'S' #초기 화재 인도 모빌리티 방향을 아래로 잡음

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

def save_grid_to_json(file_path, grid):
    """
    그리드를 JSON 파일로 저장하는 함수
    
    Args:
    - file_path: JSON 파일 경로
    - grid: 저장할 그리드 데이터
    """
    with open(file_path, 'w') as f:
        json.dump(grid, f)


def main():
    grid.create_and_save_grid(init_path)  # 초기 그리드 생성 및 저장

    # A* 알고리즘 실행 및 경로 확인
    if run_a_star(init_path, grid.start, grid.goal) is None:
        print("Can't find path")
        print("Failed to reach the destination. Calling the rescue team...")
        print("Rescue team called!")

    # JSON 파일 불러오기
    path_data = load_json("path.json")
    directions_data = load_json("directions.json")

    # JSON 데이터 출력
    print("Loaded path from JSON:")
    print(path_data["path"])
    print("\nLoaded directions from JSON:")
    print(directions_data["directions"])

    #go_drive()

    

if __name__ == "__main__":
    main()
