import json
from heapq import heappop, heappush  # 힙큐 모듈을 사용하여 우선순위 큐 구현

# 휴리스틱 함수: 맨해튼 거리를 사용하여 두 점 사이의 거리를 계산
def heuristic_manhattan(a, b):
    """
    맨해튼 거리를 계산하는 함수
    
    a: 첫 번째 점 (튜플 형태)
    b: 두 번째 점 (튜플 형태)
    반환값: 두 점 사이의 맨해튼 거리
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# 방향 벡터를 문자로 표현하는 함수
def direction_to_char(direction):
    """
    방향 벡터를 문자로 변환하는 함수
    
    direction: 방향 벡터 (튜플 형태)
    반환값: 방향을 나타내는 문자
    """
    directions = {
        (-1, 0): 'N',  # 북쪽
        (1, 0): 'S',   # 남쪽
        (0, -1): 'W',  # 서쪽
        (0, 1): 'E',   # 동쪽
        (-1, -1): 'H', # 북서쪽
        (-1, 1): 'J',  # 북동쪽
        (1, -1): 'Z',  # 남서쪽
        (1, 1): 'X'    # 남동쪽
    }
    return directions[direction]

# 목표점에 도달 가능한지 확인하는 함수
def is_goal_reachable(came_from, goal):
    """
    목표점에 도달 가능한지 확인하는 함수
    
    came_from: 각 노드의 이전 노드 정보가 저장된 딕셔너리
    goal: 목표점 (튜플 형태)
    반환값: 목표점에 도달 가능하면 True, 불가능하면 False
    """
    return goal in came_from

# A* 탐색 알고리즘 함수
def a_star_search(grid, start, goal):
    """
    A* 알고리즘을 사용하여 최단 경로를 찾는 함수
    
    grid: 2차원 배열로 표현된 그리드
    start: 시작점 (튜플 형태)
    goal: 목표점 (튜플 형태)
    반환값: 시작점에서 목표점까지의 최단 경로 리스트 (튜플 형태의 좌표들로 구성)
           도달지에 도달할 수 없을 경우 None을 반환
    """
    came_from = {}  # 각 노드의 이전 노드를 기록하여 경로를 재구성
    direction_from = {}  # 각 노드의 이전 방향을 기록하여 경로를 재구성
    cost_so_far = {}  # 시작점에서 각 노드까지의 비용을 기록
    frontier = []  # 탐색할 노드를 저장할 우선순위 큐
    heappush(frontier, (0, start))  # 시작점을 큐에 추가
    came_from[start] = None  # 시작점의 이전 노드는 없음
    cost_so_far[start] = 0  # 시작점까지의 비용은 0

    while frontier:  # 탐색할 노드가 있는 동안 반복
        current_cost, current = heappop(frontier)  # 우선순위 큐에서 비용이 가장 낮은 노드를 추출

        if current == goal:  # 목표점에 도달하면 탐색 종료
            break

        # 상하좌우 및 대각선 방향으로 이웃 노드 탐색
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            next = (current[0] + direction[0], current[1] + direction[1])  # 다음 노드의 좌표 계산
            # 그리드 내에 있고 장애물이 없는 경우에만 다음 노드로 이동
            if 0 <= next[0] < len(grid) and 0 <= next[1] < len(grid[0]) and grid[next[0]][next[1]] == 0:
                new_cost = cost_so_far[current] + 1  # 이웃 노드까지의 새로운 비용 계산
                if next not in cost_so_far or new_cost < cost_so_far[next]:  # 더 낮은 비용으로 이웃 노드를 방문할 수 있는 경우
                    cost_so_far[next] = new_cost  # 이웃 노드까지의 비용 업데이트
                    priority = new_cost + heuristic_manhattan(goal, next)  # 우선순위 계산 (비용 + 휴리스틱)
                    heappush(frontier, (priority, next))  # 우선순위 큐에 이웃 노드 추가
                    came_from[next] = current  # 이웃 노드의 이전 노드 기록
                    direction_from[next] = direction  # 이웃 노드의 이전 방향 기록

    if not is_goal_reachable(came_from, goal):  # 목표점에 도달할 수 없는 경우
        return None

    path, directions = reconstruct_path(came_from, direction_from, start, goal)  # 경로 재구성
    return path, directions  # 최단 경로 및 방향 반환

# 최적 경로 재구성 함수
def reconstruct_path(came_from, direction_from, start, goal):
    """
    최적 경로를 재구성하는 함수
    
    came_from: 각 노드의 이전 노드 정보가 저장된 딕셔너리
    direction_from: 각 노드의 이전 방향 정보가 저장된 딕셔너리
    start: 시작점 (튜플 형태)
    goal: 목표점 (튜플 형태)
    반환값: 시작점에서 목표점까지의 최단 경로 리스트 (튜플 형태의 좌표들로 구성) 및 방향 리스트
    """
    path = []
    directions = []
    current = goal
    while current != start:  # 시작점에 도달할 때까지 경로를 추적
        if current not in came_from:
            break  # 경로가 존재하지 않는 경우
        path.append(current)  # 현재 노드를 경로에 추가
        directions.append(direction_from[current])  # 현재 노드의 방향을 경로에 추가
        current = came_from[current]  # 이전 노드로 이동
    path.append(start)  # 시작점을 경로에 추가
    path.reverse()  # 경로를 시작점에서 목표점까지의 순서로 정렬
    directions.reverse()  # 방향도 경로와 같은 순서로 정렬
    direction_chars = [direction_to_char(d) for d in directions]  # 방향을 문자로 변환
    return path, direction_chars  # 최단 경로 및 방향 반환
