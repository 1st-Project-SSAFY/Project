import json
from heapq import heappop, heappush

# 맨해튼 거리 계산
def manhattan_distance(point1, point2):
    """
    두 점 사이의 맨해튼 거리를 계산합니다.
    
    :param point1: 첫 번째 점 (튜플 형태)
    :param point2: 두 번째 점 (튜플 형태)
    :return: 두 점 사이의 맨해튼 거리
    """
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# 방향 벡터를 문자로 변환
def direction_to_char(direction):
    """
    방향 벡터를 문자로 변환합니다.
    
    :param direction: 방향 벡터 (튜플 형태)
    :return: 방향을 나타내는 문자
    """
    direction_map = {
        (-1, 0): 'N',  # 북쪽
        (1, 0): 'S',   # 남쪽
        (0, -1): 'W',  # 서쪽
        (0, 1): 'E',   # 동쪽
        (-1, -1): 'H', # 북서쪽
        (-1, 1): 'J',  # 북동쪽
        (1, -1): 'Z',  # 남서쪽
        (1, 1): 'X'    # 남동쪽
    }
    return direction_map[direction]

# 목표점에 도달 가능 여부 확인
def is_reachable(came_from, goal):
    """
    목표점에 도달 가능한지 확인합니다.
    
    :param came_from: 각 노드의 이전 노드 정보가 저장된 딕셔너리
    :param goal: 목표점 (튜플 형태)
    :return: 목표점에 도달 가능하면 True, 그렇지 않으면 False
    """
    return goal in came_from

# A* 알고리즘을 사용하여 최단 경로 탐색
def a_star_search(grid, start, goal):
    """
    A* 알고리즘을 사용하여 최단 경로를 찾습니다.
    
    :param grid: 2차원 배열로 표현된 그리드
    :param start: 시작점 (튜플 형태)
    :param goal: 목표점 (튜플 형태)
    :return: 최단 경로 (튜플 리스트) 및 방향 문자 리스트. 도달 불가능할 경우 None 반환
    """
    came_from = {}        # 각 노드의 이전 노드 정보
    direction_from = {}   # 각 노드의 이전 방향 정보
    cost_so_far = {}      # 시작점에서 각 노드까지의 비용
    frontier = []         # 탐색할 노드를 저장할 우선순위 큐

    heappush(frontier, (0, start))  # 시작점을 큐에 추가
    came_from[start] = None         # 시작점의 이전 노드는 없음
    cost_so_far[start] = 0          # 시작점까지의 비용은 0

    while frontier:
        current_cost, current = heappop(frontier)  # 비용이 가장 낮은 노드를 추출

        if current == goal:
            break

        # 가능한 방향 벡터
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])  # 이웃 노드의 좌표 계산

            if (0 <= neighbor[0] < len(grid) and
                0 <= neighbor[1] < len(grid[0]) and
                grid[neighbor[0]][neighbor[1]] == 0):
                
                new_cost = cost_so_far[current] + 1  # 이웃 노드까지의 새로운 비용 계산
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + manhattan_distance(goal, neighbor)
                    heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current
                    direction_from[neighbor] = direction

    if not is_reachable(came_from, goal):
        return None

    return reconstruct_path(came_from, direction_from, start, goal)

# 최적 경로 및 방향 재구성
def reconstruct_path(came_from, direction_from, start, goal):
    """
    최적 경로를 재구성합니다.
    
    :param came_from: 각 노드의 이전 노드 정보
    :param direction_from: 각 노드의 이전 방향 정보
    :param start: 시작점 (튜플 형태)
    :param goal: 목표점 (튜플 형태)
    :return: 최단 경로 (튜플 리스트) 및 방향 문자 리스트
    """
    path = []
    directions = []
    current = goal

    while current != start:
        if current not in came_from:
            break
        path.append(current)
        directions.append(direction_from[current])
        current = came_from[current]

    path.append(start)
    path.reverse()
    directions.reverse()
    
    direction_chars = [direction_to_char(d) for d in directions]
    return path, direction_chars
