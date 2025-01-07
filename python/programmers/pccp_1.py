"""
[PCCP 기출문제] 1번 / 동영상 재생기
굳이 분/초로 나누지 않고 초의 총합으로 전환하는 아이디어가 중요했음. 나머지는 구현에 집중
"""


def time_to_sec(timestamp: str):
    m, s = map(int, timestamp.split(':'))
    return 60 * m + s


def solution(video_len, pos, op_start, op_end, commands):
    pos_sec = time_to_sec(pos)
    video_len_sec = time_to_sec(video_len)
    op_start_sec = time_to_sec(op_start)
    op_end_sec = time_to_sec(op_end)

    if op_start_sec <= pos_sec <= op_end_sec:
        pos_sec = op_end_sec

    for cmd in commands:
        if cmd == "prev":
            pos_sec -= 10
        else:
            pos_sec += 10
        if pos_sec < 0:
            pos_sec = 0
        elif pos_sec > video_len_sec:
            pos_sec = video_len_sec
        if op_start_sec <= pos_sec <= op_end_sec:
            pos_sec = op_end_sec
        print(f"pos: {pos_sec}")

    answer = f"{pos_sec//60:02}:{pos_sec%60:02}"
    return answer