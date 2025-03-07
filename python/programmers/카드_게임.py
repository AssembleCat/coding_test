def solution(coin, cards):
    n = len(cards)
    target_sum = n + 1
    
    # 초기에 가지고 있는 카드 (n/3장)
    initial_hand = cards[:n//3]
    
    # 남은 카드
    remaining_cards = cards[n//3:]
    
    # 메모이제이션을 위한 캐시
    # 키: (라운드 인덱스, 손에 있는 카드 튜플, 보류 중인 카드 튜플, 남은 동전 수)
    # 값: 최대 라운드 수
    cache = {}
    
    def dfs(round_idx, hand, pending, remaining, coins_left):
        # 남은 카드가 2장 미만이면 더 이상 진행할 수 없음
        if len(remaining) < 2:
            return round_idx
        
        # 캐시 키 생성
        cache_key = (round_idx, tuple(sorted(hand)), tuple(sorted(pending)), coins_left)
        
        # 이미 계산된 결과가 있으면 반환
        if cache_key in cache:
            return cache[cache_key]
        
        # 새로 뽑은 두 장의 카드
        new_card1, new_card2 = remaining[0], remaining[1]
        new_remaining = remaining[2:]
        
        # 가능한 모든 선택지를 탐색
        max_rounds = round_idx  # 기본값: 현재 라운드에서 종료
        
        # 1. 새 카드 두 장 모두 버리는 경우
        new_pending = pending + [new_card1, new_card2]
        
        # 1-1. 손에 있는 카드로만 라운드 진행
        for i in range(len(hand)):
            for j in range(i+1, len(hand)):
                if hand[i] + hand[j] == target_sum:
                    new_hand = hand.copy()
                    new_hand.remove(hand[i])
                    new_hand.remove(hand[j])
                    max_rounds = max(max_rounds, dfs(round_idx + 1, new_hand, new_pending, new_remaining, coins_left))
        
        # 1-2. 손에 있는 카드 + 보류 중인 카드 하나로 라운드 진행
        if coins_left >= 1:
            for card in hand:
                for p_card in new_pending:
                    if card + p_card == target_sum:
                        new_hand = hand.copy()
                        new_hand.remove(card)
                        new_p = new_pending.copy()
                        new_p.remove(p_card)
                        max_rounds = max(max_rounds, dfs(round_idx + 1, new_hand, new_p, new_remaining, coins_left - 1))
        
        # 1-3. 보류 중인 카드 두 장으로 라운드 진행
        if coins_left >= 2:
            for i in range(len(new_pending)):
                for j in range(i+1, len(new_pending)):
                    if new_pending[i] + new_pending[j] == target_sum:
                        new_p = new_pending.copy()
                        new_p.remove(new_pending[i])
                        new_p.remove(new_pending[j])
                        max_rounds = max(max_rounds, dfs(round_idx + 1, hand, new_p, new_remaining, coins_left - 2))
        
        # 2. 새 카드 중 하나만 가져가는 경우 (동전 1개 사용)
        if coins_left >= 1:
            # 2-1. 첫 번째 카드만 가져가는 경우
            new_hand = hand + [new_card1]
            new_pending = pending + [new_card2]
            
            # 손에 있는 카드로만 라운드 진행
            for i in range(len(new_hand)):
                for j in range(i+1, len(new_hand)):
                    if new_hand[i] + new_hand[j] == target_sum:
                        next_hand = new_hand.copy()
                        next_hand.remove(new_hand[i])
                        next_hand.remove(new_hand[j])
                        max_rounds = max(max_rounds, dfs(round_idx + 1, next_hand, new_pending, new_remaining, coins_left - 1))
            
            # 2-2. 두 번째 카드만 가져가는 경우
            new_hand = hand + [new_card2]
            new_pending = pending + [new_card1]
            
            # 손에 있는 카드로만 라운드 진행
            for i in range(len(new_hand)):
                for j in range(i+1, len(new_hand)):
                    if new_hand[i] + new_hand[j] == target_sum:
                        next_hand = new_hand.copy()
                        next_hand.remove(new_hand[i])
                        next_hand.remove(new_hand[j])
                        max_rounds = max(max_rounds, dfs(round_idx + 1, next_hand, new_pending, new_remaining, coins_left - 1))
        
        # 3. 새 카드 두 장 모두 가져가는 경우 (동전 2개 사용)
        if coins_left >= 2:
            new_hand = hand + [new_card1, new_card2]
            
            # 손에 있는 카드로만 라운드 진행
            for i in range(len(new_hand)):
                for j in range(i+1, len(new_hand)):
                    if new_hand[i] + new_hand[j] == target_sum:
                        next_hand = new_hand.copy()
                        next_hand.remove(new_hand[i])
                        next_hand.remove(new_hand[j])
                        max_rounds = max(max_rounds, dfs(round_idx + 1, next_hand, pending, new_remaining, coins_left - 2))
        
        # 결과 캐싱
        cache[cache_key] = max_rounds
        return max_rounds
    
    # DFS 시작
    return dfs(0, initial_hand, [], remaining_cards, coin)


# 테스트
def test_solution():
    # 예제 테스트 케이스
    coin = 4
    cards = [3, 6, 7, 2, 1, 10, 5, 9, 8, 12, 11, 4]
    result = solution(coin, cards)
    expected = 5
    print(f"결과: {result}, 기대값: {expected}, {'성공' if result == expected else '실패'}")

if __name__ == "__main__":
    test_solution()
