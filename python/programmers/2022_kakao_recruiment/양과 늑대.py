def solution(info, edges):
    # 트리 구조 생성
    tree = [[] for _ in range(len(info))]
    for parent, child in edges:
        tree[parent].append(child)
    
    # 방문한 상태를 저장할 집합 (메모이제이션)
    # 상태: (양 수, 늑대 수, 방문 가능한 노드 집합을 비트마스크로 표현)
    # 비트마스크는 노드 수가 최대 17개이므로 정수로 충분히 표현 가능
    visited = set()
    
    # 최대 양 수를 저장할 변수
    max_sheep = 0
    
    def dfs(current_node_set, sheep, wolf):
        nonlocal max_sheep
        
        # 현재 양의 수가 최대값보다 크면 업데이트
        max_sheep = max(max_sheep, sheep)
        
        # 방문 가능한 다음 노드 집합 생성
        next_nodes = set()
        
        # 현재 방문한 노드들로부터 갈 수 있는 자식 노드들 추가
        for node in range(len(info)):
            if (current_node_set & (1 << node)) > 0:  # 현재 노드 집합에 node가 있으면
                for child in tree[node]:
                    next_nodes.add(child)
        
        # 이미 방문한 노드는 제외 (현재 노드 집합에 없는 노드들만 남김)
        next_nodes = [node for node in next_nodes if not (current_node_set & (1 << node))]
        
        # 각 다음 노드에 대해 DFS 수행
        for next_node in next_nodes:
            next_sheep = sheep
            next_wolf = wolf
            
            # 다음 노드에 있는 동물 정보 업데이트
            if info[next_node] == 0:  # 양
                next_sheep += 1
            else:  # 늑대
                next_wolf += 1
            
            # 늑대가 양보다 많으면 진행하지 않음
            if next_wolf >= next_sheep:
                continue
            
            # 다음 노드 집합 생성
            next_node_set = current_node_set | (1 << next_node)
            
            # 이미 방문한 상태면 진행하지 않음
            state = (next_sheep, next_wolf, next_node_set)
            if state in visited:
                continue
            
            visited.add(state)
            
            # DFS 재귀 호출
            dfs(next_node_set, next_sheep, next_wolf)
    
    # 루트 노드(0번)부터 시작
    initial_node_set = 1  # 비트마스크로 0번 노드 표시 (2^0 = 1)
    initial_sheep = 1     # 루트 노드는 항상 양
    initial_wolf = 0
    
    # 초기 상태 방문 표시
    visited.add((initial_sheep, initial_wolf, initial_node_set))
    
    # DFS 탐색 시작
    dfs(initial_node_set, initial_sheep, initial_wolf)
    
    return max_sheep

# 테스트 케이스
if __name__ == "__main__":
    # 예제 1
    info1 = [0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1]
    edges1 = [[0, 1], [1, 2], [1, 4], [0, 8], [8, 7], [9, 10], [9, 11], [4, 3], [6, 5], [4, 6], [8, 9]]
    print(solution(info1, edges1))  # 예상 결과: 5
    
    # 예제 2
    info2 = [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
    edges2 = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [4, 8], [6, 9], [9, 10]]
    print(solution(info2, edges2))  # 예상 결과: 5
