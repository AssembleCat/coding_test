from collections import deque

def solution(board):
    n = len(board)
    
    # 로봇의 초기 상태: (로봇의 두 위치, 방향, 이동 시간)
    # 방향: 0은 가로, 1은 세로
    # 문제에서는 1-indexed이지만 코드에서는 0-indexed로 변환
    start = ((0, 0), (0, 1), 0, 0)  # ((r1, c1), (r2, c2), 방향, 시간)
    
    # 방문한 상태 저장 (두 위치와 방향)
    visited = set()
    
    # BFS를 위한 큐
    queue = deque([start])
    
    # 이동 방향 (상, 하, 좌, 우)
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    
    while queue:
        (r1, c1), (r2, c2), direction, time = queue.popleft()
        
        # 목적지 도착 확인 (로봇의 두 칸 중 하나라도 목적지에 도착)
        if (r1 == n-1 and c1 == n-1) or (r2 == n-1 and c2 == n-1):
            return time
        
        # 이미 방문한 상태인지 확인
        state = ((r1, c1), (r2, c2), direction)
        if state in visited:
            continue
        
        # 방문 상태 기록
        visited.add(state)
        
        # 1. 상하좌우 이동
        for i in range(4):
            nr1, nc1 = r1 + dr[i], c1 + dc[i]
            nr2, nc2 = r2 + dr[i], c2 + dc[i]
            
            # 이동 가능 여부 확인 (지도 범위 내, 벽이 아님)
            if 0 <= nr1 < n and 0 <= nc1 < n and 0 <= nr2 < n and 0 <= nc2 < n:
                if board[nr1][nc1] == 0 and board[nr2][nc2] == 0:
                    queue.append(((nr1, nc1), (nr2, nc2), direction, time + 1))
        
        # 2. 회전
        # 가로 방향인 경우 (로봇이 가로로 놓여 있음)
        if direction == 0:
            # 왼쪽 칸을 축으로 회전
            # 위로 회전
            if r1 > 0 and board[r1-1][c1] == 0 and board[r1-1][c2] == 0:
                queue.append(((r1, c1), (r1-1, c1), 1, time + 1))
            # 아래로 회전
            if r1 < n-1 and board[r1+1][c1] == 0 and board[r1+1][c2] == 0:
                queue.append(((r1, c1), (r1+1, c1), 1, time + 1))
                
            # 오른쪽 칸을 축으로 회전
            # 위로 회전
            if r2 > 0 and board[r2-1][c1] == 0 and board[r2-1][c2] == 0:
                queue.append(((r2, c2), (r2-1, c2), 1, time + 1))
            # 아래로 회전
            if r2 < n-1 and board[r2+1][c1] == 0 and board[r2+1][c2] == 0:
                queue.append(((r2, c2), (r2+1, c2), 1, time + 1))
        
        # 세로 방향인 경우 (로봇이 세로로 놓여 있음)
        else:
            # 위쪽 칸을 축으로 회전
            # 왼쪽으로 회전
            if c1 > 0 and board[r1][c1-1] == 0 and board[r2][c1-1] == 0:
                queue.append(((r1, c1), (r1, c1-1), 0, time + 1))
            # 오른쪽으로 회전
            if c1 < n-1 and board[r1][c1+1] == 0 and board[r2][c1+1] == 0:
                queue.append(((r1, c1), (r1, c1+1), 0, time + 1))
                
            # 아래쪽 칸을 축으로 회전
            # 왼쪽으로 회전
            if c2 > 0 and board[r1][c2-1] == 0 and board[r2][c2-1] == 0:
                queue.append(((r2, c2), (r2, c2-1), 0, time + 1))
            # 오른쪽으로 회전
            if c2 < n-1 and board[r1][c2+1] == 0 and board[r2][c2+1] == 0:
                queue.append(((r2, c2), (r2, c2+1), 0, time + 1))
    
    # 목적지에 도달할 수 없는 경우 (문제에서는 항상 도달 가능하다고 함)
    return -1

# 예제 테스트 케이스
if __name__ == "__main__":
    board = [
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0]
    ]
    
    print(f"예상 결과: 7, 실제 결과: {solution(board)}")
