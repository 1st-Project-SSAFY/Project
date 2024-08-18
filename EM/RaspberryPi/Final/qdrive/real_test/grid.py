import json

# 맵의 크기
rows, cols = 20, 26
# 맵을 초기화 (모든 값을 0으로 설정)
grid = [[0] * cols for _ in range(rows)]

# 시작점과 목표점 초기화
start = (2, 24)
goal = (19, 17)

# 장애물 설정 함수
def set_obstacles():
    """
    그리드에 장애물을 설정하는 함수
    
    장애물은 그리드 내에서 특정 범위에 해당하는 좌표를 1로 설정하여 표시됨.
    """
    # 0행의 0열부터 17열까지의 값을 1로 설정
    for col in range(18):
        grid[0][col] = 1

    # 0행부터 8행까지의 22열부터 25열까지의 값을 1로 설정
    for row in range(9):  # 0행부터 8행까지
        if row == 2:
            continue
        for col in range(22, 26):  # 22열부터 25열까지
            grid[row][col] = 1

    # 3행부터 6행까지의 1열부터 4열까지의 값을 1로 설정
    for row in range(3, 7):  # 3행부터 6행까지
        for col in range(1, 5):  # 1열부터 4열까지
            grid[row][col] = 1

    # 8행부터 11행까지의 1열부터 4열까지의 값을 1로 설정
    for row in range(8, 12):  # 8행부터 11행까지
        for col in range(1, 5):  # 1열부터 4열까지
            grid[row][col] = 1

    # 12행부터 19행까지의 0열부터 15열까지의 값을 1로 설정
    for row in range(12, 20):  # 12행부터 19행까지
        for col in range(16):  # 0열부터 15열까지
            grid[row][col] = 1

    # 6열부터 16열까지의 3행부터 9행까지의 값을 1로 설정
    for row in range(3, 10):  # 3행부터 9행까지
        for col in range(6, 17):  # 6열부터 16열까지
            grid[row][col] = 1

    # 9행부터 16행까지의 25열을 1로 설정
    for row in range(9, 17):  # 9행부터 16행까지
        grid[row][25] = 1


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
    grid = [[0] * cols for _ in range(rows)]  # 20x26 크기의 0으로 초기화된 2차원 배열 생성
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
