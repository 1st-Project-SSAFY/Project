import json  # JSON 모듈 임포트
from astar import a_star_search  # A* 알고리즘을 사용하여 최단 경로를 찾는 함수 임포트
from grid import grid, start, goal  # 사용할 그리드와 시작 및 목표 위치를 임포트

def print_path_matrix(grid, path, directions=None, visited=None):
    """
    그리드와 경로, 방문한 위치를 출력하는 함수.
    
    Args:
        grid (list of list): 2차원 배열로 표현된 그리드
        path (list of tuples): 최단 경로를 나타내는 좌표 리스트
        directions (list of str, optional): 경로의 방향 리스트. 기본값은 None
        visited (set of tuples, optional): 방문한 위치 집합. 기본값은 None
    """
    path_set = set(path)  # 경로를 집합으로 변환하여 검색 효율화
    visited = visited or set()  # 방문한 위치가 없으면 빈 집합으로 초기화
    direction_map = {}
    
    if directions:
        for i in range(len(path) - 1):
            direction_map[path[i]] = directions[i]


    for i in range(len(grid)):  # 그리드의 행을 순회
        for j in range(len(grid[0])):  # 그리드의 열을 순회
            position = (i, j)
            if position == start:
                print("S", end=" ")  # 시작점 표시
            elif position == goal:
                print("G", end=" ")  # 목표점 표시
            elif position in path_set:
                print(direction_map.get(position, "P"), end=" ")  # 경로의 방향 또는 "P" 표시
            elif position in visited:
                print(".", end=" ")  # 방문한 위치 표시
            else:
                print(grid[i][j], end=" ")  # 그리드의 원래 값 출력
        print()
    print()

def save_to_json(file_path, data):
    """
    데이터를 JSON 형식으로 저장하는 함수.
    
    Args:
        file_path (str): JSON 파일 경로
        data (dict): 저장할 데이터
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def run_a_star(grid_file, start, goal):
    """
    A* 알고리즘을 실행하고 결과를 JSON 파일로 저장하는 함수.
    
    Args:
        grid_file (str): 그리드가 저장된 JSON 파일 경로
        start (tuple): 시작 위치
        goal (tuple): 목표 위치

    Returns:
        int: 성공 시 1, 실패 시 None
    """
    global grid
    grid = load_grid_from_json(grid_file)  # 그리드 로드

    path, directions = a_star_search(grid, start, goal)
    
    if path is None:
        return None  # 경로를 찾지 못한 경우
    
    # 최종 경로 및 방향 문자 출력
    print("\nFinal path:")
    print_path_matrix(grid, path, directions)
    
    direction_chars = directions  # 방향 문자 리스트
    print("Direction characters along the path:")
    print(direction_chars)
    
    # JSON 형식으로 경로와 방향 문자 저장
    save_to_json("/home/a204/qdrive/real_test/path.json", {"path": path})
    save_to_json("/home/a204/qdrive/real_test/path_copy.json", {"path": path})
    save_to_json("/home/a204/qdrive/real_test/directions.json", {"directions": direction_chars})
    

    return 1

def load_grid_from_json(file_path):
    """
    JSON 파일에서 그리드를 로드하는 함수.
    
    Args:
        file_path (str): JSON 파일 경로

    Returns:
        list of list: 로드된 그리드
    """
    with open(file_path, 'r') as file:
        return json.load(file)
