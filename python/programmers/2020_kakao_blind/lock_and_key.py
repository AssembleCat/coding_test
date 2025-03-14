def solution(key, lock):
    m = len(key)
    n = len(lock)
    
    # 열쇠를 시계 방향으로 90도 회전하는 함수
    def rotate_90(key):
        new_key = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                new_key[j][m-1-i] = key[i][j]
        return new_key
    
    # 확장된 자물쇠 생성 (열쇠가 자물쇠 영역을 벗어나는 경우 처리)
    expanded_size = n + 2 * (m - 1)
    expanded_lock = [[0] * expanded_size for _ in range(expanded_size)]
    
    # 확장된 자물쇠의 중앙에 원래 자물쇠 배치
    for i in range(n):
        for j in range(n):
            expanded_lock[i + m - 1][j + m - 1] = lock[i][j]
    
    # 자물쇠에 홈이 몇 개인지 계산 (모든 홈이 채워졌는지 확인용)
    lock_holes = sum(row.count(0) for row in lock)
    
    # 열쇠를 0, 90, 180, 270도 회전시켜 확인
    rotated_key = key
    for _ in range(4):
        # 열쇠를 모든 가능한 위치에 배치하여 확인
        for i in range(expanded_size - m + 1):
            for j in range(expanded_size - m + 1):
                # 현재 위치와 회전 상태에서 자물쇠를 열 수 있는지 확인
                if check_unlock(rotated_key, expanded_lock, i, j, m, n, lock_holes):
                    return True
        
        # 열쇠를 90도 회전
        rotated_key = rotate_90(rotated_key)
    
    return False

def check_unlock(key, expanded_lock, start_i, start_j, m, n, lock_holes):
    # 실제 자물쇠 영역의 범위
    lock_start_i = m - 1
    lock_start_j = m - 1
    lock_end_i = lock_start_i + n
    lock_end_j = lock_start_j + n
    
    # 열쇠와 자물쇠를 겹치는 부분 확인
    filled_holes = 0  # 채워진 홈의 개수
    
    for i in range(m):
        for j in range(m):
            # 현재 열쇠 위치가 실제 자물쇠 영역 내에 있는지 확인
            lock_i = start_i + i
            lock_j = start_j + j
            
            if lock_start_i <= lock_i < lock_end_i and lock_start_j <= lock_j < lock_end_j:
                # 자물쇠 영역 내에 있는 경우
                if key[i][j] == 1 and expanded_lock[lock_i][lock_j] == 1:
                    # 열쇠의 돌기와 자물쇠의 돌기가 만나는 경우 (불가능)
                    return False
                elif key[i][j] == 1 and expanded_lock[lock_i][lock_j] == 0:
                    # 열쇠의 돌기가 자물쇠의 홈을 채우는 경우
                    filled_holes += 1
    
    # 모든 홈이 채워졌는지 확인
    return filled_holes == lock_holes

# 테스트
if __name__ == "__main__":
    key = [[0, 0, 0], [1, 0, 0], [0, 1, 1]]
    lock = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
    print(solution(key, lock))  # True 출력
