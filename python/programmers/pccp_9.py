"""
[PCCE 기출문제] 9번 / 지폐 접기
"""


def solution(wallet, bill):
    answer = 0
    while min(wallet) < min(bill) or max(wallet) < max(bill):
        answer += 1
        if bill[0] > bill[1]:
            bill[0] //= 2
        else:
            bill[1] //= 2
    return answer


if __name__ == '__main__':
    solution([30, 15], [26, 17])
