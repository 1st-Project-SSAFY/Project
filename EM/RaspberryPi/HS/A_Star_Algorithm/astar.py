# astar.py

from heapq import heappop, heappush

# 휴리스틱 함수: 맨해튼 거리를 사용하여 두 점 사이의 거리를 계산
def heuristic_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* 탐색 알고리즘 함수
def a_star_search(grid, start, goal):
    came_from = {}
    cost_so_far = {}
    frontier = []
    heappush(frontier, (0, start))
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current_cost, current = heappop(frontier)

        if current == goal:
            break

        for next in neighbors(current, grid):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic_manhattan(goal, next)
                heappush(frontier, (priority, next))
                came_from[next] = current

    path = reconstruct_path(came_from, start, goal)
    return path

# 이웃 노드 찾기 함수: 상하좌우 및 대각선 방향
def neighbors(node, grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    neighbors = []
    for direction in directions:
        neighbor = (node[0] + direction[0], node[1] + direction[1])
        if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] == 0:
            neighbors.append(neighbor)
    return neighbors

# 최적 경로 재구성 함수
def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:
        if current not in came_from:
            break  # 경로가 존재하지 않는 경우
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()  # start에서 goal까지의 순서로 정렬
    return path
