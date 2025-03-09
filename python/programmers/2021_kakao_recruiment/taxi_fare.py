def solution(n, s, a, b, fares):
    """
    n: 지점 개수
    s: 출발 지점
    a: A의 도착 지점
    b: B의 도착 지점
    fares: 지점 간 택시 요금 [출발, 도착, 요금]
    """
    # 플로이드-워셜 알고리즘을 위한 인접 행렬 초기화
    # 무한대 값으로 초기화 (Python에서는 float('inf')로 표현)
    INF = float('inf')
    dist = [[INF] * (n+1) for _ in range(n+1)]
    
    # 자기 자신으로 가는 비용은 0으로 초기화
    for i in range(1, n+1):
        dist[i][i] = 0
    
    # 주어진 요금 정보로 인접 행렬 채우기
    for c, d, f in fares:
        dist[c][d] = f
        dist[d][c] = f  # 양방향 그래프
    
    # 플로이드-워셜 알고리즘 수행
    for k in range(1, n+1):  # 경유 지점
        for i in range(1, n+1):  # 출발 지점
            for j in range(1, n+1):  # 도착 지점
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # 최소 비용 계산 (합승 여부에 따라)
    min_cost = dist[s][a] + dist[s][b]  # 합승하지 않는 경우
    
    # 모든 지점을 합승 하차 지점으로 고려
    for k in range(1, n+1):
        # s에서 k까지 합승한 후, k에서 각자의 목적지로 가는 비용 계산
        cost = dist[s][k] + dist[k][a] + dist[k][b]
        min_cost = min(min_cost, cost)
    
    return min_cost

# 테스트 케이스
if __name__ == "__main__":
    # 예시 1
    test1 = solution(6, 4, 6, 2, [[4, 1, 10], [3, 5, 24], [5, 6, 2], [3, 1, 41], [5, 1, 24], [4, 6, 50], [2, 4, 66], [2, 3, 22], [1, 6, 25]])
    print(f"예시 1 결과: {test1}, 예상 결과: 82")
    
    # 예시 2
    test2 = solution(7, 3, 4, 1, [[5, 7, 9], [4, 6, 4], [3, 6, 1], [3, 2, 3], [2, 1, 6]])
    print(f"예시 2 결과: {test2}, 예상 결과: 14")
    
    # 예시 3
    test3 = solution(6, 4, 5, 6, [[2, 6, 6], [6, 3, 7], [4, 6, 7], [6, 5, 11], [2, 5, 12], [5, 3, 20], [2, 4, 8], [4, 3, 9]])
    print(f"예시 3 결과: {test3}, 예상 결과: 18")
