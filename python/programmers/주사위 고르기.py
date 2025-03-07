def solution(dice):
    n = len(dice)
    half = n // 2
    
    # 모든 가능한 A의 주사위 조합 생성
    from itertools import combinations
    a_combinations = list(combinations(range(n), half))
    
    max_win_prob = -1
    best_combination = None
    
    for a_dice_indices in a_combinations:
        a_dice_indices = list(a_dice_indices)
        b_dice_indices = [i for i in range(n) if i not in a_dice_indices]
        
        # A와 B의 주사위 조합
        a_dices = [dice[i] for i in a_dice_indices]
        b_dices = [dice[i] for i in b_dice_indices]
        
        # 각 조합에서 승/무/패 계산
        win, draw, lose = calculate_outcomes(a_dices, b_dices)
        total_cases = win + draw + lose
        win_prob = win / total_cases
        
        if win_prob > max_win_prob:
            max_win_prob = win_prob
            best_combination = a_dice_indices
    
    # 주사위 번호는 1부터 시작하므로 1을 더해줌
    return [i + 1 for i in sorted(best_combination)]

def calculate_outcomes(a_dices, b_dices):
    # A의 모든 가능한 주사위 합과 경우의 수 계산
    a_sums = get_all_possible_sums(a_dices)
    
    # B의 모든 가능한 주사위 합과 경우의 수 계산
    b_sums = get_all_possible_sums(b_dices)
    
    win, draw, lose = 0, 0, 0
    
    # B의 합을 정렬하여 누적 합 계산을 위한 준비
    sorted_b_sums = sorted(b_sums.items())
    total_cases = sum(count for _, count in sorted_b_sums)
    
    # A의 각 합에 대해 승/무/패 계산
    for a_sum, a_count in a_sums.items():
        # 현재 A의 합보다 작은 B의 합이 있는 경우 (A 승리)
        less_than_a = 0
        equal_to_a = 0
        
        for b_sum, b_count in sorted_b_sums:
            if b_sum < a_sum:
                less_than_a += b_count
            elif b_sum == a_sum:
                equal_to_a = b_count
            else:
                # b_sum > a_sum인 경우는 더 이상 계산할 필요 없음
                break
        
        # A가 이기는 경우: B의 합이 A보다 작은 모든 경우
        win += a_count * less_than_a
        
        # 무승부인 경우: A의 합과 B의 합이 같은 경우
        draw += a_count * equal_to_a
        
        # A가 지는 경우: B의 합이 A보다 큰 모든 경우
        greater_than_a = total_cases - less_than_a - equal_to_a
        lose += a_count * greater_than_a
    
    return win, draw, lose

def get_all_possible_sums(dices):
    # 초기값: 빈 주사위 (합이 0, 경우의 수 1)
    sums = {0: 1}
    
    # 각 주사위에 대해 가능한 모든 합 계산
    for dice in dices:
        new_sums = {}
        for current_sum, count in sums.items():
            for face in dice:
                new_sum = current_sum + face
                new_sums[new_sum] = new_sums.get(new_sum, 0) + count
        sums = new_sums
    
    return sums

# 테스트
if __name__ == "__main__":
    # 예제 테스트
    dice = [[1, 2, 3, 4, 5, 6], [3, 3, 3, 3, 4, 4], [1, 3, 3, 4, 4, 4], [1, 1, 4, 4, 5, 5]]
    print(solution(dice))  # [1, 4]
    
    # 엣지 케이스 테스트
    # 모든 주사위가 동일한 경우
    dice2 = [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
    print(solution(dice2))  # [1]
    
    # 주사위 수가 많은 경우 (성능 테스트)
    import random
    random.seed(42)  # 재현 가능한 결과를 위한 시드 설정
    large_dice = [[random.randint(1, 6) for _ in range(6)] for _ in range(10)]
    print(solution(large_dice))
