import json

# 맵의 크기
width = 51
height = 40

# 맵을 초기화 (모든 값을 0으로 설정)
grid = [[0 for _ in range(width)] for _ in range(height)]

# 시작점과 목표점 초기화
start = (3, 0)
goal = (39, 31)

# 장애물 설정 함수
def set_obstacles():
    """
    그리드에 장애물을 설정하는 함수
    
    장애물은 그리드 내에서 특정 범위에 해당하는 좌표를 1로 설정하여 표시됨.
    """
    # 첫 번째 지정된 영역을 1로 채우기
    for row in range(3):  # 0행부터 2행까지
        for col in range(36):  # 0열부터 35열까지
            grid[row][col] = 1

    # 두 번째 지정된 영역을 1로 채우기
    for row in range(17):  # 0행부터 16행까지
        for col in range(43, 51):  # 43열부터 50열까지
            grid[row][col] = 1

    # 세 번째 지정된 영역을 1로 채우기
    for row in range(17, 32):  # 17행부터 31행까지
        for col in range(48, 51):  # 48열부터 50열까지
            grid[row][col] = 1

    # 추가된 영역을 1로 채우기
    for row in range(7, 15):  # 7행부터 14행까지
        for col in range(2, 9):  # 2열부터 8열까지
            grid[row][col] = 1

    # 새로 추가된 영역을 1로 채우기
    for row in range(17, 25):  # 17행부터 24행까지
        for col in range(2, 9):  # 2열부터 8열까지
            grid[row][col] = 1

    # 최종 요구 사항에 따라 추가된 영역을 1로 채우기
    for row in range(25, 40):  # 25행부터 39행까지
        for col in range(30):  # 0열부터 29열까지
            grid[row][col] = 1

    # 추가된 영역을 1로 채우기 (최종 요구 사항)
    for row in range(7, 21):  # 7행부터 20행까지
        for col in range(13, 36):  # 13열부터 35열까지
            grid[row][col] = 1

# JSON 파일로 저장하는 함수
def save_grid_to_json(file_path):
    """
    그리드를 JSON 파일로 저장하는 함수
    
    file_path: JSON 파일의 경로
    """
    with open(file_path, 'w') as f:
        json.dump(grid, f)

# 초기화 함수
def initialize_grid():
    """
    그리드를 초기화하는 함수
    
    장애물을 설정하고 설정된 그리드를 JSON 파일로 저장함.
    """
    global grid  # 전역 변수 grid를 사용
    grid = [[0 for _ in range(width)] for _ in range(height)]  # 45x45 크기의 0으로 초기화된 2차원 배열 생성
    set_obstacles()  # 장애물 설정

def print_grid(grid):
    """
    그리드를 출력하는 함수
    
    grid: 출력할 2차원 배열
    """
    for row in grid:
        print(' '.join(map(str, row)))  # 각 행을 공백을 사이에 두고 출력

def create_and_save_grid(file_path):
    """
    그리드를 초기화하고 JSON 파일로 저장하는 함수
    
    file_path: JSON 파일의 경로
    """
    initialize_grid()  # 그리드 초기화
    save_grid_to_json(file_path)  # 그리드를 JSON 파일로 저장
    
    # 저장된 JSON 파일을 로드하여 출력
    with open(file_path, 'r') as f:
        loaded_grid = json.load(f)

    print(" ")
    print("Initial Grid:")
    print_grid(loaded_grid)  # 초기화된 그리드 출력
