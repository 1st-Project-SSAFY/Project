# grid.py

# 45x45 크기의 0으로 초기화된 2차원 배열 생성
grid = [[0] * 45 for _ in range(45)]

# 장애물 설정
for i in range(10, 25):
    for j in range(7, 17):
        grid[i][j] = 1

for i in range(30, 32):
    for j in range(7, 17):
        grid[i][j] = 1

for i in range(0, 39):
    for j in range(25, 45):
        grid[i][j] = 1

start = (1, 1)   # 시작점 좌표
goal = (44, 35)  # 목표점 좌표
