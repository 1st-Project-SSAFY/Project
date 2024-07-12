# main.py

from astar import a_star_search
from grid import grid, start, goal

# 경로 행렬을 출력하는 함수
def print_path_matrix(grid, path, visited=None):
    path_set = set(path)
    if visited is None:
        visited = set()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) == start:
                print("S", end=" ")  # 시작점 표시
            elif (i, j) == goal:
                print("G", end=" ")  # 목표점 표시
            elif (i, j) in path_set:
                print("P", end=" ")  # 최단 경로 표시
            elif (i, j) in visited:
                print(".", end=" ")  # 방문한 위치 표시
            else:
                print(grid[i][j], end=" ")
        print()
    print()

# 예제 사용법
if __name__ == "__main__":
    visited = set()  # 방문한 위치 기록할 집합

    # A* 알고리즘을 사용하여 최단 경로를 찾음
    print("Start:")
    print_path_matrix(grid, [], visited)
    path = a_star_search(grid, start, goal)
    
    # 움직이면서 경로 추적
    for position in path:
        visited.add(position)
        print("\nMoving to:", position)
        print_path_matrix(grid, path, visited)
    
    print("\nFinal path:")
    print_path_matrix(grid, path, visited)  # 최단 경로 출력
