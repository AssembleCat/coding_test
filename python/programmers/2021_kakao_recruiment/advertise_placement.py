def solution(play_time, adv_time, logs):
    # 시간을 초 단위로 변환하는 함수
    def time_to_seconds(time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    
    # 초를 시간 문자열로 변환하는 함수
    def seconds_to_time(seconds):
        h, seconds = divmod(seconds, 3600)
        m, s = divmod(seconds, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    
    # 시간 변환
    play_time_sec = time_to_seconds(play_time)
    adv_time_sec = time_to_seconds(adv_time)
    
    # 모든 시간대의 시청자 수 변화를 기록할 배열 (0초부터 play_time_sec까지)
    time_line = [0] * (play_time_sec + 1)
    
    # 각 로그에 대해 시작 시간에 +1, 종료 시간에 -1을 기록
    for log in logs:
        start_time, end_time = log.split('-')
        start_sec = time_to_seconds(start_time)
        end_sec = time_to_seconds(end_time)
        
        time_line[start_sec] += 1
        time_line[end_sec] -= 1
    
    # 누적 합으로 각 시간대의 시청자 수 계산
    for i in range(1, len(time_line)):
        time_line[i] += time_line[i-1]
    
    # 누적 합으로 각 시간대까지의 누적 시청 시간 계산
    # 이 배열의 [t] 값은 0초부터 t초까지의 누적 시청 시간
    total_time = [0] * (play_time_sec + 1)
    for i in range(1, len(time_line)):
        total_time[i] = total_time[i-1] + time_line[i-1]
    
    # 광고 구간의 최대 누적 시청 시간과 해당 시작 시간 찾기
    max_view_time = 0
    max_start_time = 0
    
    # 가능한 모든 광고 시작 시간에 대해 확인
    for start_time in range(play_time_sec - adv_time_sec + 1):
        end_time = start_time + adv_time_sec
        view_time = total_time[end_time] - total_time[start_time]
        
        if view_time > max_view_time:
            max_view_time = view_time
            max_start_time = start_time
    
    return seconds_to_time(max_start_time)

# 테스트 케이스
if __name__ == "__main__":
    # 테스트 케이스 1
    play_time = "02:03:55"
    adv_time = "00:14:15"
    logs = ["01:20:15-01:45:14", "00:40:31-01:00:00", "00:25:50-00:48:29", "01:30:59-01:53:29", "01:37:44-02:02:30"]
    expected = "01:30:59"
    result = solution(play_time, adv_time, logs)
    print(f"테스트 케이스 1 결과: {result}, 기대값: {expected}, {'성공' if result == expected else '실패'}")
    
    # 테스트 케이스 2
    play_time = "99:59:59"
    adv_time = "25:00:00"
    logs = ["69:59:59-89:59:59", "01:00:00-21:00:00", "79:59:59-99:59:59", "11:00:00-31:00:00"]
    expected = "01:00:00"
    result = solution(play_time, adv_time, logs)
    print(f"테스트 케이스 2 결과: {result}, 기대값: {expected}, {'성공' if result == expected else '실패'}")
    
    # 테스트 케이스 3
    play_time = "50:00:00"
    adv_time = "50:00:00"
    logs = ["15:36:51-38:21:49", "10:14:18-15:36:51", "38:21:49-42:51:45"]
    expected = "00:00:00"
    result = solution(play_time, adv_time, logs)
    print(f"테스트 케이스 3 결과: {result}, 기대값: {expected}, {'성공' if result == expected else '실패'}")
