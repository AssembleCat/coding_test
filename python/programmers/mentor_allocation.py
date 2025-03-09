def solution(k, n, reqs):
    """
    k: 상담 유형의 수
    n: 멘토의 총 수
    reqs: 참가자 상담 요청 정보 [시작시간, 상담시간, 상담유형]
    """
    # 각 유형별 요청 분리
    type_requests = [[] for _ in range(k+1)]
    for req in reqs:
        start_time, duration, req_type = req
        type_requests[req_type].append((start_time, duration))
    
    # 초기 최소 배분: 각 유형별로 1명씩 배정
    mentor_counts = [0] * (k+1)  # 0번 인덱스는 사용하지 않음
    remaining = n
    
    # 최소 대기 시간
    min_waiting_time = float('inf')
    
    # 모든 가능한 멘토 배분 조합을 탐색하는 재귀 함수
    def dfs(type_idx, remaining_mentors):
        nonlocal min_waiting_time
        
        # 모든 유형에 멘토 배분 완료
        if type_idx > k:
            # 각 유형별 대기 시간 계산
            total_wait = 0
            for t in range(1, k+1):
                total_wait += calculate_waiting_time(type_requests[t], mentor_counts[t])
            
            # 최소 대기 시간 업데이트
            min_waiting_time = min(min_waiting_time, total_wait)
            return
        
        # 이전 유형까지 할당한 상태에서 이미 최소값보다 크면 더 이상 탐색할 필요 없음 (가지치기)
        current_wait = 0
        for t in range(1, type_idx):
            current_wait += calculate_waiting_time(type_requests[t], mentor_counts[t])
        if current_wait >= min_waiting_time:
            return
        
        # 현재 유형에 할당할 수 있는 멘토 수 범위
        min_count = 1  # 각 유형에 최소 1명
        max_count = remaining_mentors - (k - type_idx)  # 남은 유형에도 최소 1명씩 할당
        
        # 마지막 유형이면 남은 모든 멘토 할당
        if type_idx == k:
            mentor_counts[type_idx] = remaining_mentors
            dfs(type_idx + 1, 0)
            mentor_counts[type_idx] = 0
            return
        
        # 현재 유형에 멘토 할당 시도
        for count in range(min_count, max_count + 1):
            mentor_counts[type_idx] = count
            dfs(type_idx + 1, remaining_mentors - count)
        
        mentor_counts[type_idx] = 0
    
    # DFS 시작 (첫 번째 유형부터)
    dfs(1, n)
    
    return min_waiting_time

def calculate_waiting_time(requests, num_mentors):
    """
    특정 유형의 요청들과 해당 유형에 할당된 멘토 수를 받아 총 대기 시간 계산
    """
    if not requests or num_mentors == 0:
        return 0
    
    # 멘토별 가용 시간 (상담 종료 시간)
    mentor_end_times = [0] * num_mentors
    
    # 총 대기 시간
    total_waiting_time = 0
    
    # 각 요청에 대해 처리
    for start_time, duration in sorted(requests):
        # 가장 빨리 이용 가능한 멘토 찾기
        earliest_available_idx = 0
        for i in range(1, num_mentors):
            if mentor_end_times[i] < mentor_end_times[earliest_available_idx]:
                earliest_available_idx = i
        
        # 대기 시간 계산
        waiting_time = max(0, mentor_end_times[earliest_available_idx] - start_time)
        total_waiting_time += waiting_time
        
        # 멘토 가용 시간 업데이트
        consultation_start_time = max(start_time, mentor_end_times[earliest_available_idx])
        mentor_end_times[earliest_available_idx] = consultation_start_time + duration
    
    return total_waiting_time
