def solution(users, emoticons):
    """
    이모티콘 할인 행사에서 최적의 할인율 조합을 찾는 함수
    
    Args:
        users: 사용자 정보 배열 [할인율 기준, 가격 기준]
        emoticons: 이모티콘 가격 배열
    
    Returns:
        [이모티콘 플러스 가입자 수, 이모티콘 판매액]
    """
    # 가능한 할인율
    discount_rates = [10, 20, 30, 40]
    
    # 최적의 결과를 저장할 변수
    max_subscribers = 0
    max_sales = 0
    
    # 모든 이모티콘에 대한 할인율 조합을 생성하는 재귀 함수
    def find_best_combination(index, discounts):
        nonlocal max_subscribers, max_sales
        
        # 모든 이모티콘에 대한 할인율이 정해졌을 때
        if index == len(emoticons):
            subscribers = 0
            sales = 0
            
            # 각 사용자별로 계산
            for user_discount, user_price in users:
                user_purchase = 0
                
                # 사용자가 구매하는 이모티콘 계산
                for i, emoticon_price in enumerate(emoticons):
                    # 할인율이 사용자 기준 이상이면 구매
                    if discounts[i] >= user_discount:
                        # 할인된 가격으로 구매
                        discounted_price = emoticon_price * (100 - discounts[i]) // 100
                        user_purchase += discounted_price
                
                # 구매 금액이 기준 이상이면 이모티콘 플러스 가입
                if user_purchase >= user_price:
                    subscribers += 1
                else:
                    sales += user_purchase
            
            # 최적의 결과 갱신
            # 1. 가입자 수가 더 많은 경우
            # 2. 가입자 수가 같고 판매액이 더 큰 경우
            if subscribers > max_subscribers or (subscribers == max_subscribers and sales > max_sales):
                max_subscribers = subscribers
                max_sales = sales
            
            return
        
        # 현재 이모티콘에 대해 모든 할인율 시도
        for rate in discount_rates:
            discounts[index] = rate
            find_best_combination(index + 1, discounts)
    
    # 초기 할인율 배열 생성 후 재귀 호출
    initial_discounts = [0] * len(emoticons)
    find_best_combination(0, initial_discounts)
    
    return [max_subscribers, max_sales]

# 테스트
if __name__ == "__main__":
    # 테스트 케이스 1
    users1 = [[40, 10000], [25, 10000]]
    emoticons1 = [7000, 9000]
    result1 = solution(users1, emoticons1)
    print(f"테스트 케이스 1 결과: {result1}, 기대값: [1, 5400]")
    
    # 테스트 케이스 2
    users2 = [[40, 2900], [23, 10000], [11, 5200], [5, 5900], [40, 3100], [27, 9200], [32, 6900]]
    emoticons2 = [1300, 1500, 1600, 4900]
    result2 = solution(users2, emoticons2)
    print(f"테스트 케이스 2 결과: {result2}, 기대값: [4, 13860]")
