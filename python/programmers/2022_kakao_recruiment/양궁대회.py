def solution(n, info):
    # 점수 계산 함수
    def calculate_score(apeach_info, ryan_info):
        apeach_score = 0
        ryan_score = 0
        
        for i in range(11):
            # i번째 인덱스는 10-i점을 의미
            if apeach_info[i] == 0 and ryan_info[i] == 0:
                continue  # 둘 다 맞추지 못한 경우
            
            # 각 점수에 대해 더 많은 화살을 맞힌 선수가 점수 획득
            if apeach_info[i] >= ryan_info[i]:
                apeach_score += 10 - i
            else:
                ryan_score += 10 - i
                
        return ryan_score - apeach_score  # 라이언과 어피치의 점수 차이 반환
    
    # 백트래킹을 통한 가능한 모든 조합 탐색
    max_diff = 0  # 최대 점수 차이
    max_ryan_info = []  # 최대 점수 차이를 내는 라이언의 화살 배치
    
    def dfs(idx, arrows_left, ryan_info):
        nonlocal max_diff, max_ryan_info
        
        # 모든 점수(0~10)에 대해 화살 배치를 결정한 경우
        if idx == 11:
            # 화살을 모두 사용하지 않은 경우는 고려하지 않음
            if arrows_left > 0:
                return
            
            score_diff = calculate_score(info, ryan_info)
            
            # 라이언이 이기는 경우만 고려
            if score_diff > 0:
                # 더 큰 점수 차이를 내는 경우 업데이트
                if score_diff > max_diff:
                    max_diff = score_diff
                    max_ryan_info = ryan_info.copy()
                # 동일한 점수 차이인 경우, 낮은 점수에 더 많은 화살을 할당한 경우 선택
                elif score_diff == max_diff:
                    # 낮은 점수부터 비교 (뒤에서부터)
                    for i in range(10, -1, -1):
                        if ryan_info[i] > max_ryan_info[i]:
                            max_ryan_info = ryan_info.copy()
                            break
                        elif ryan_info[i] < max_ryan_info[i]:
                            break
            return
        
        # 화살을 모두 사용한 경우
        if arrows_left == 0:
            dfs(11, 0, ryan_info.copy())
            return
            
        # 현재 점수에 화살을 쏘지 않는 경우
        dfs(idx + 1, arrows_left, ryan_info.copy())
        
        # 현재 점수에 화살을 쏘는 경우 (어피치보다 1개 더 쏨)
        if arrows_left >= info[idx] + 1:
            new_ryan_info = ryan_info.copy()
            new_ryan_info[idx] = info[idx] + 1
            dfs(idx + 1, arrows_left - (info[idx] + 1), new_ryan_info)
        
        # 마지막 점수(0점)이고 남은 화살이 있는 경우, 모두 사용
        if idx == 10 and arrows_left > 0:
            new_ryan_info = ryan_info.copy()
            new_ryan_info[10] = arrows_left
            dfs(11, 0, new_ryan_info)
    
    # 백트래킹 시작
    dfs(0, n, [0] * 11)
    
    # 라이언이 이길 수 없는 경우
    if not max_ryan_info:
        return [-1]
    
    return max_ryan_info

# 테스트 코드
if __name__ == "__main__":
    # 테스트 케이스
    test_cases = [
        (5, [2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]),  # [0, 2, 2, 0, 1, 0, 0, 0, 0, 0, 0]
        (1, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # [-1]
        (9, [0, 0, 1, 2, 0, 1, 1, 1, 1, 1, 1]),  # [1, 1, 2, 0, 1, 2, 2, 0, 0, 0, 0]
        (10, [0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 3])  # [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2]
    ]
    
    for i, (n, info) in enumerate(test_cases):
        result = solution(n, info)
        print(f"테스트 케이스 {i+1}: {result}")
