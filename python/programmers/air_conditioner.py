def solution(temperature, t1, t2, a, b, onboard):
    # 온도 값에 오프셋 추가하여 음수 온도 처리
    OFFSET = 100  # 충분히 큰 오프셋
    t_offset = temperature + OFFSET
    t1_offset = t1 + OFFSET
    t2_offset = t2 + OFFSET
    
    # 가능한 온도 범위 설정
    temp_min = min(t1, temperature) - 10  # 여유 있게 설정
    temp_max = max(t2, temperature) + 10
    temp_range = temp_max - temp_min + 1
    
    # dp[시간][온도][에어컨 상태] = 최소 전력 소비량
    # 에어컨 상태: 0=꺼짐, 1=켜짐
    INF = float('inf')
    dp = [[[INF for _ in range(2)] for _ in range(temp_range)] for _ in range(len(onboard))]
    
    # 초기 상태: 0분의 온도는 실외온도와 같음
    temp_idx = temperature - temp_min
    dp[0][temp_idx][0] = 0  # 에어컨 꺼짐
    dp[0][temp_idx][1] = b  # 에어컨 켜짐 (실내온도=희망온도)
    
    for time in range(1, len(onboard)):
        for curr_temp in range(temp_min, temp_max + 1):
            curr_idx = curr_temp - temp_min
            
            # 가능한 모든 이전 온도에 대해 탐색
            for prev_temp in range(temp_min, temp_max + 1):
                prev_idx = prev_temp - temp_min
                
                # 온도 변화가 1도를 초과하면 불가능
                if abs(curr_temp - prev_temp) > 1:
                    continue
                
                # 에어컨이 꺼져 있을 때의 온도 변화 (실외온도 방향으로만 변화 가능)
                if prev_temp < temperature and curr_temp == prev_temp + 1:
                    # 이전에 에어컨이 꺼져 있던 경우
                    if dp[time-1][prev_idx][0] != INF:
                        dp[time][curr_idx][0] = min(dp[time][curr_idx][0], dp[time-1][prev_idx][0])
                    # 이전에 에어컨이 켜져 있다가 끈 경우
                    if dp[time-1][prev_idx][1] != INF:
                        dp[time][curr_idx][0] = min(dp[time][curr_idx][0], dp[time-1][prev_idx][1])
                
                elif prev_temp > temperature and curr_temp == prev_temp - 1:
                    # 이전에 에어컨이 꺼져 있던 경우
                    if dp[time-1][prev_idx][0] != INF:
                        dp[time][curr_idx][0] = min(dp[time][curr_idx][0], dp[time-1][prev_idx][0])
                    # 이전에 에어컨이 켜져 있다가 끈 경우
                    if dp[time-1][prev_idx][1] != INF:
                        dp[time][curr_idx][0] = min(dp[time][curr_idx][0], dp[time-1][prev_idx][1])
                
                elif prev_temp == temperature and curr_temp == temperature:
                    # 이전에 에어컨이 꺼져 있던 경우
                    if dp[time-1][prev_idx][0] != INF:
                        dp[time][curr_idx][0] = min(dp[time][curr_idx][0], dp[time-1][prev_idx][0])
                    # 이전에 에어컨이 켜져 있다가 끈 경우
                    if dp[time-1][prev_idx][1] != INF:
                        dp[time][curr_idx][0] = min(dp[time][curr_idx][0], dp[time-1][prev_idx][1])
                
                # 에어컨이 켜져 있을 때 (온도는 희망온도 방향으로 변화)
                
                # 이전에 에어컨이 꺼져 있다가 켜는 경우
                if dp[time-1][prev_idx][0] != INF:
                    # 온도가 같은 경우 (희망온도를 현재 온도로 설정)
                    if curr_temp == prev_temp:
                        dp[time][curr_idx][1] = min(dp[time][curr_idx][1], dp[time-1][prev_idx][0] + b)
                    
                    # 온도가 변하는 경우 (희망온도를 더 낮거나 높게 설정)
                    # 이 경우 희망온도는 현재 온도와 다르므로 a 전력 소비
                    elif abs(curr_temp - prev_temp) == 1:
                        # 희망온도를 현재 온도보다 낮게/높게 설정해서 온도가 변하는 상황
                        dp[time][curr_idx][1] = min(dp[time][curr_idx][1], dp[time-1][prev_idx][0] + a)
                
                # 이전에도 에어컨이 켜져 있었던 경우
                if dp[time-1][prev_idx][1] != INF:
                    # 온도가 같은 경우 (희망온도를 현재 온도로 설정)
                    if curr_temp == prev_temp:
                        dp[time][curr_idx][1] = min(dp[time][curr_idx][1], dp[time-1][prev_idx][1] + b)
                    
                    # 온도가 변하는 경우 (희망온도를 더 낮거나 높게 설정)
                    elif abs(curr_temp - prev_temp) == 1:
                        dp[time][curr_idx][1] = min(dp[time][curr_idx][1], dp[time-1][prev_idx][1] + a)
        
        # 승객이 탑승 중인 시간에는 온도가 t1~t2 범위 내에 있어야 함
        if onboard[time] == 1:
            for temp in range(temp_min, temp_max + 1):
                temp_idx = temp - temp_min
                if temp < t1 or temp > t2:
                    dp[time][temp_idx][0] = INF
                    dp[time][temp_idx][1] = INF
    
    # 마지막 시간에 가능한 모든 온도에서 최소 전력 소비 찾기
    min_power = INF
    for temp in range(temp_min, temp_max + 1):
        temp_idx = temp - temp_min
        min_power = min(min_power, dp[-1][temp_idx][0], dp[-1][temp_idx][1])
    
    return min_power
