def solution(n, bans):
    # 삭제된 주문 집합
    banned_spells = set(bans)

    # 인덱스를 문자열로 변환
    def index_to_string(idx):
        # 문자열 길이 결정
        length = 1
        total = 0
        while True:
            count = 26 ** length
            if total + count > idx:
                break
            total += count
            length += 1
        
        # 해당 길이에서의 인덱스 계산
        idx_in_length = idx - total
        
        # 문자열 생성
        result = ""
        for i in range(length):
            char_idx = idx_in_length // (26 ** (length - i - 1))
            result += chr(ord('a') + char_idx)
            idx_in_length %= (26 ** (length - i - 1))
        
        return result
    
    # 문자열을 인덱스로 변환
    def string_to_index(s):
        length = len(s)
        # 이전 길이의 모든 문자열 개수
        idx = sum(26 ** i for i in range(1, length))
        
        # 현재 길이에서의 인덱스 계산
        for i, char in enumerate(s):
            char_idx = ord(char) - ord('a')
            idx += char_idx * (26 ** (length - i - 1))
        
        return idx
    
    # 삭제된 주문들을 인덱스로 변환하고 정렬
    banned_indices = sorted([string_to_index(ban) for ban in banned_spells])
    
    # 이진 탐색으로 특정 값보다 작거나 같은 요소의 개수 계산
    def count_less_or_equal(arr, val):
        left, right = 0, len(arr)
        while left < right:
            mid = (left + right) // 2
            if arr[mid] <= val:
                left = mid + 1
            else:
                right = mid
        return left
    
    # 이진 탐색으로 n번째 주문 찾기
    target = n - 1  # 0-based 인덱스로 변환
    left = 0
    right = sum(26 ** i for i in range(1, 12))  # 최대 11자리까지의 모든 문자열 개수
    
    while left < right:
        mid = (left + right) // 2
        
        # mid 인덱스까지 삭제된 주문의 개수 계산 (이진 탐색 사용)
        banned_count = count_less_or_equal(banned_indices, mid)
        
        # 실제 인덱스 계산
        actual_index = mid - banned_count
        
        if actual_index < target:
            left = mid + 1
        else:
            right = mid
    
    # 결과 문자열 생성
    result = index_to_string(left)
    
    # 결과가 삭제된 주문인 경우 다음 유효한 주문 찾기
    while result in banned_spells:
        left += 1
        result = index_to_string(left)
    
    return result
