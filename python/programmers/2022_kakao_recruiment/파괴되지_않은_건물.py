def solution(board, skill):
    n = len(board)      # 행의 수
    m = len(board[0])   # 열의 수
    
    # 변화량을 기록할 배열 초기화
    changes = [[0] * (m+1) for _ in range(n+1)]
    
    # 각 스킬에 대한 변화량 기록
    for s in skill:
        type, r1, c1, r2, c2, degree = s
        
        # type이 1이면 공격(-), 2면 회복(+)
        value = -degree if type == 1 else degree
        
        # 직사각형 영역의 시작점과 끝점만 마킹
        changes[r1][c1] += value
        changes[r1][c2+1] -= value
        changes[r2+1][c1] -= value
        changes[r2+1][c2+1] += value
    
    # 행 방향으로 누적 합 계산
    for i in range(n+1):
        for j in range(1, m+1):
            changes[i][j] += changes[i][j-1]
    
    # 열 방향으로 누적 합 계산
    for j in range(m+1):
        for i in range(1, n+1):
            changes[i][j] += changes[i-1][j]
    
    # 원래 맵에 변화량 적용 및 파괴되지 않은 건물 개수 계산
    answer = 0
    for i in range(n):
        for j in range(m):
            if board[i][j] + changes[i][j] > 0:
                answer += 1
    
    return answer

# 테스트
if __name__ == "__main__":
    # 예제 1
    board1 = [
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5]
    ]
    skill1 = [
        [1, 0, 0, 3, 4, 4],
        [1, 2, 0, 2, 3, 2],
        [2, 1, 0, 3, 1, 2],
        [1, 0, 1, 3, 3, 1]
    ]
    print(solution(board1, skill1))  # 기대 결과: 10
    
    # 예제 2
    board2 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    skill2 = [
        [1, 1, 1, 2, 2, 4],
        [1, 0, 0, 1, 1, 2],
        [2, 2, 0, 2, 0, 100]
    ]
    print(solution(board2, skill2))  # 기대 결과: 6
