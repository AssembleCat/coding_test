from collections import Counter
from itertools import combinations

def solution(orders, course):
    answer = []
    
    # 각 코스 크기별로 처리
    for course_size in course:
        # 가능한 모든 메뉴 조합 생성
        order_combinations = []
        for order in orders:
            # 주문된 메뉴를 정렬하여 동일한 조합을 일관되게 표현
            sorted_order = ''.join(sorted(order))
            # 주문 길이가 코스 크기보다 크거나 같은 경우에만 조합 생성
            if len(sorted_order) >= course_size:
                order_combinations.extend(combinations(sorted_order, course_size))
        
        # 생성된 조합을 문자열로 변환하고 빈도 계산
        combination_counter = Counter([''.join(combo) for combo in order_combinations])
        
        # 조합 중 가장 많이 주문된 빈도수 확인
        if combination_counter:
            max_count = max(combination_counter.values())
            # 빈도수가 2 이상인 경우에만 처리
            if max_count >= 2:
                answer.extend([''.join(combo) for combo, count in combination_counter.items() if count == max_count])
    
    # 결과를 사전순으로 정렬
    return sorted(answer)

# 테스트 케이스 실행
if __name__ == "__main__":
    test_cases = [
        {
            "orders": ["ABCFG", "AC", "CDE", "ACDE", "BCFG", "ACDEH"],
            "course": [2, 3, 4],
            "expected": ["AC", "ACDE", "BCFG", "CDE"]
        },
        {
            "orders": ["ABCDE", "AB", "CD", "ADE", "XYZ", "XYZ", "ACD"],
            "course": [2, 3, 5],
            "expected": ["ACD", "AD", "ADE", "CD", "XYZ"]
        },
        {
            "orders": ["XYZ", "XWY", "WXA"],
            "course": [2, 3, 4],
            "expected": ["WX", "XY"]
        }
    ]
    
    for i, tc in enumerate(test_cases):
        result = solution(tc["orders"], tc["course"])
        print(f"테스트 케이스 {i+1}:")
        print(f"예상 결과: {tc['expected']}")
        print(f"실제 결과: {result}")
        print(f"결과: {'성공' if result == tc['expected'] else '실패'}")
        print()
