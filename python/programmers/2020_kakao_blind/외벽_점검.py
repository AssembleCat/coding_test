from itertools import permutations

def solution(n, weak, dist):
    # 취약 지점 개수
    weak_len = len(weak)
    
    # 원형 구조를 선형으로 변환 (weak 배열 확장)
    linear_weak = weak + [w + n for w in weak]
    
    # 답이 없는 경우를 위한 초기값 설정
    answer = len(dist) + 1
    
    # 각 취약 지점을 시작점으로 설정
    for start in range(weak_len):
        # dist 배열의 모든 순열 고려
        for friends in permutations(dist, len(dist)):
            # 투입할 친구 수
            count = 1
            # 현재 친구가 점검할 수 있는 마지막 위치
            position = linear_weak[start] + friends[0]
            
            # 모든 취약 지점 확인
            for i in range(start + 1, start + weak_len):
                # 현재 친구가 다음 취약 지점을 점검할 수 없는 경우
                if position < linear_weak[i]:
                    count += 1
                    # 더 투입할 친구가 없는 경우
                    if count > len(dist):
                        break
                    # 다음 친구를 투입하여 해당 취약 지점부터 점검
                    position = linear_weak[i] + friends[count - 1]
            
            # 모든 취약 지점을 점검할 수 있는 경우, 최소값 갱신
            if count <= len(dist):
                answer = min(answer, count)
    
    # 모든 친구를 투입해도 점검할 수 없는 경우
    if answer > len(dist):
        return -1
    
    return answer

# 테스트 케이스
print(solution(12, [1, 5, 6, 10], [1, 2, 3, 4]))  # 2
print(solution(12, [1, 3, 4, 9, 10], [3, 5, 7]))  # 1
