import json  # JSON 모듈 임포트
from astar import a_star_search  # A* 알고리즘을 사용하여 최단 경로를 찾는 함수 임포트
from grid import grid, start, goal  # 사용할 그리드와 시작 및 목표 위치를 임포트

# 경로 행렬을 출력하는 함수
def print_path_matrix(grid, path, directions=None, visited=None):
    """
    그리드와 경로, 방문한 위치를 받아서 출력하는 함수
    
    grid: 2차원 배열로 표현된 그리드
    path: 최단 경로 리스트 (튜플 형태의 좌표들로 구성)
    directions: 경로의 방향 리스트 (옵션, 기본값은 None)
    visited: 방문한 위치 집합 (옵션, 기본값은 None)
    """
    path_set = set(path)  # 경로를 집합으로 변환하여 효율적으로 검색
    if visited is None:
        visited = set()  # 방문한 위치가 없으면 빈 집합으로 초기화
    direction_map = {}
    if directions:
        for i in range(len(path) - 1):
            direction_map[path[i]] = directions[i]
    for i in range(len(grid)):  # 그리드의 행을 순회
        for j in range(len(grid[0])):  # 그리드의 열을 순회
            if (i, j) == start:
                print("S", end=" ")  # 시작점 표시
            elif (i, j) == goal:
                print("G", end=" ")  # 목표점 표시
            elif (i, j) in path_set:
                if (i, j) in direction_map:
                    print(direction_map[(i, j)], end=" ")  # 경로의 방향 표시
                else:
                    print("P", end=" ")  # 최단 경로 표시
            elif (i, j) in visited:
                print(".", end=" ")  # 방문한 위치 표시
            else:
                print(grid[i][j], end=" ")  # 그리드의 원래 값 출력
        print()
    print()

def extract_direction_chars(directions):
    """
    경로의 방향 문자를 저장하는 배열을 반환하는 함수
    
    directions: 경로의 방향 리스트
    반환값: 방향 문자 리스트
    """
    return directions

def save_path_to_json(file_path, path):
    """
    최적 경로를 JSON 형식으로 저장하는 함수
    
    file_path: JSON 파일 경로
    path: 최적 경로 리스트
    """
    data = {"path": path}
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def save_directions_to_json(file_path, directions):
    """
    방향 문자 리스트를 JSON 형식으로 저장하는 함수
    
    file_path: JSON 파일 경로
    directions: 방향 문자 리스트
    """
    data = {"directions": directions}
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# 그리드를 JSON 파일로부터 로드하는 함수
def load_grid_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def run_a_star(grid_file, start, goal):
    """
    A* 알고리즘을 실행하고 결과를 JSON 파일로 저장하는 함수
    """

    global grid
    grid = load_grid_from_json(grid_file)  # 그리드 로드

    visited = set()  # 방문한 위치를 기록할 집합 초기화

    # A* 알고리즘을 사용하여 최단 경로를 찾음
    if a_star_search(grid, start, goal) != None:
        path, directions = a_star_search(grid, start, goal)
    else:
        return None

    # 디버깅용 중간 경로 추적 (주석 처리된 부분)
    # for position in path:
    #     visited.add(position)  # 방문한 위치 추가
    #     print("\nMoving to:", position)  # 현재 위치 출력
    #     print_path_matrix(grid, path, visited)  # 현재 경로 상태 출력
    
    # 최종 경로 출력
    print(" ")
    print("Final path:")
    print_path_matrix(grid, path, directions)  # 최단 경로 출력
    
    # 최단 경로의 방향 문자 저장
    direction_chars = extract_direction_chars(directions)
    
    # 방향 문자 리스트 출력
    print("Direction characters along the path:")
    print(direction_chars)
    
    # 최적 경로를 JSON 형식으로 저장
    save_path_to_json("path.json", path)
    
    # 방향 문자 리스트를 JSON 형식으로 저장
    save_directions_to_json("directions.json", direction_chars)

    return 1
