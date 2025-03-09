from collections import deque

def solution(board, r, c):
    # 보드에서 카드 위치 파악
    card_positions = {}
    for i in range(4):
        for j in range(4):
            if board[i][j] > 0:
                num = board[i][j]
                if num not in card_positions:
                    card_positions[num] = []
                card_positions[num].append((i, j))
    
    # 모든 카드 쌍의 번호 리스트
    card_numbers = list(card_positions.keys())
    
    # 현재 커서 위치에서 목표 위치까지의 최소 이동 횟수 계산 (BFS)
    def find_min_moves(current_board, start, end):
        sr, sc = start
        er, ec = end
        
        # 이미 같은 위치면 0 반환
        if sr == er and sc == ec:
            return 0
        
        # BFS 탐색
        queue = deque([(sr, sc, 0)])  # (행, 열, 이동 횟수)
        visited = {(sr, sc)}
        
        # 방향: 상, 하, 좌, 우
        dr = [-1, 1, 0, 0]
        dc = [0, 0, -1, 1]
        
        while queue:
            r, c, cnt = queue.popleft()
            
            # 목표 위치에 도달한 경우
            if r == er and c == ec:
                return cnt
            
            # 1. 상하좌우 한 칸 이동
            for i in range(4):
                nr, nc = r + dr[i], c + dc[i]
                
                # 보드 범위 내이고 아직 방문하지 않은 곳이면
                if 0 <= nr < 4 and 0 <= nc < 4 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, cnt + 1))
            
            # 2. Ctrl + 방향키 이동
            for i in range(4):
                nr, nc = r, c
                
                # 해당 방향으로 쭉 이동
                while True:
                    nr += dr[i]
                    nc += dc[i]
                    
                    # 보드를 벗어나면 그 전 위치로
                    if nr < 0 or nr >= 4 or nc < 0 or nc >= 4:
                        nr -= dr[i]
                        nc -= dc[i]
                        break
                    
                    # 카드를 만나면 그 위치에서 정지
                    if current_board[nr][nc] > 0:
                        break
                
                # 원래 위치와 다르고 아직 방문하지 않은 곳이면
                if (nr != r or nc != c) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, cnt + 1))
        
        return -1  # 도달 불가능한 경우
    
    # 보드에서 카드 제거
    def remove_card(b, card_num):
        new_board = [row[:] for row in b]
        for i in range(4):
            for j in range(4):
                if new_board[i][j] == card_num:
                    new_board[i][j] = 0
        return new_board
    
    # 재귀적으로 모든 카드를 제거하는 최소 비용 계산
    def find_min_cost(current_board, current_pos, cards_left, memo={}):
        # 모든 카드가 제거되었으면 0 반환
        if not cards_left:
            return 0
        
        # 메모이제이션에 저장된 값이 있으면 반환
        key = (current_pos, tuple(sorted(cards_left)))
        if key in memo:
            return memo[key]
        
        min_cost = float('inf')
        
        # 남은 각 카드에 대해 최소 비용 계산
        for card in cards_left:
            new_cards = cards_left[:]
            new_cards.remove(card)
            
            # 해당 카드의 두 위치
            pos1, pos2 = card_positions[card]
            
            # 경우 1: 현재 위치 -> pos1 -> pos2 -> 나머지 카드
            cost1 = find_min_moves(current_board, current_pos, pos1)  # 현재 위치 -> pos1
            cost1 += 1  # Enter
            cost1 += find_min_moves(current_board, pos1, pos2)  # pos1 -> pos2
            cost1 += 1  # Enter
            
            # 카드 제거 후 재귀 호출
            new_board = remove_card(current_board, card)
            cost1 += find_min_cost(new_board, pos2, new_cards, memo)
            
            # 경우 2: 현재 위치 -> pos2 -> pos1 -> 나머지 카드
            cost2 = find_min_moves(current_board, current_pos, pos2)  # 현재 위치 -> pos2
            cost2 += 1  # Enter
            cost2 += find_min_moves(current_board, pos2, pos1)  # pos2 -> pos1
            cost2 += 1  # Enter
            
            # 카드 제거 후 재귀 호출
            cost2 += find_min_cost(new_board, pos1, new_cards, memo)
            
            # 더 작은 비용 선택
            min_cost = min(min_cost, cost1, cost2)
        
        # 결과 저장 및 반환
        memo[key] = min_cost
        return min_cost
    
    # 최종 결과 반환
    return find_min_cost(board, (r, c), card_numbers)
