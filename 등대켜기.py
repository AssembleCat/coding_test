def solution(n, lighthouse):
    # 인접 리스트로 트리 구성
    graph = [[] for _ in range(n+1)]
    for a, b in lighthouse:
        graph[a].append(b)
        graph[b].append(a)
    
    # DP 값을 저장할 배열
    # dp[node][0]: node를 켜지 않았을 때 서브트리의 최소 등대 개수
    # dp[node][1]: node를 켰을 때 서브트리의 최소 등대 개수
    dp = [[0, 0] for _ in range(n+1)]
    
    # 방문 여부 체크
    visited = [False] * (n+1)
    
    def dfs(node):
        visited[node] = True
        
        # 리프 노드인 경우 (연결된 노드가 부모 하나뿐)
        is_leaf = sum(1 for child in graph[node] if not visited[child]) == 0
        if is_leaf:
            dp[node][0] = 0  # 리프 노드를 켜지 않으면 0개
            dp[node][1] = 1  # 리프 노드를 켜면 1개
            return
        
        # 이 노드를 켤 때의 최소 개수: 자식 노드는 켜도 되고 안 켜도 됨
        dp[node][1] = 1  # 자기 자신
        
        # 이 노드를 끌 때의 최소 개수: 모든 자식 노드는 반드시 켜져 있어야 함
        dp[node][0] = 0
        
        for child in graph[node]:
            if not visited[child]:
                dfs(child)
                # 자신이 켜져 있으면 자식은 켜도 되고 안 켜도 됨(최소값 선택)
                dp[node][1] += min(dp[child][0], dp[child][1])
                # 자신이 꺼져 있으면 모든 자식은 반드시 켜져 있어야 함
                dp[node][0] += dp[child][1]
    
    # 시작점을 1로 가정 (문제에서 1부터 n까지 번호 매겨짐)
    # 실제 트리에서는 루트가 특별히 정해져 있지 않으므로 임의의 노드에서 시작 가능
    dfs(1)
    
    # 루트를 켜는 경우와 끄는 경우 중 최소값 선택
    return min(dp[1][0], dp[1][1])

# 테스트 케이스
if __name__ == "__main__":
    # 예시 1
    n1 = 8
    lighthouse1 = [[1, 2], [1, 3], [1, 4], [1, 5], [5, 6], [5, 7], [5, 8]]
    print(solution(n1, lighthouse1))  # 예상 결과: 2
    
    # 예시 2
    n2 = 10
    lighthouse2 = [[4, 1], [5, 1], [5, 6], [7, 6], [1, 2], [1, 3], [6, 8], [2, 9], [9, 10]]
    print(solution(n2, lighthouse2))  # 예상 결과: 3
