def solution(m, n, puddles):
    """
    m*n 2차원 배열 생성 -> 기본값은 0으로 선언하고 puddle은 -1로 선언
    모든 elements를 순회하며 -1 이라면 생략
    0 이상이라면 현재 셀의 왼쪽, 위쪽의 값을 더함.
    """
    mat = [[0] * (m + 1) for row in range(n + 1)]  # m*n 선언

    for i, j in puddles:
        mat[i][j] = -1

    for i in range(1, n):
        for j in range(1, m):
            if mat[i][j] == -1:
                continue
            if mat[i-1][j] == -1:
                mat[i][j] ==

