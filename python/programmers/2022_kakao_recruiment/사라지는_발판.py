def solution(board, aloc, bloc):
    # 움직일 수 있는 방향 (상, 하, 좌, 우)
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    # 메모이제이션을 위한 캐시
    # 상태: (현재 위치 x, y, 상대 위치 x, y, 보드 상태)
    # 결과: (승패 여부, 턴 수)
    cache = {}
    
    # 보드의 크기
    rows, cols = len(board), len(board[0])
    
    # 보드 상태를 문자열로 변환하여 캐시의 키로 사용
    def board_to_key(board):
        return ''.join(''.join(str(cell) for cell in row) for row in board)
    
    # DFS로 게임 상태 탐색
    # x, y: 현재 플레이어 위치
    # ox, oy: 상대 플레이어 위치
    # board: 현재 보드 상태
    # turn: 현재까지의 턴 수
    # is_my_turn: 현재 내 턴인지 여부 (A 플레이어 기준)
    def dfs(x, y, ox, oy, current_board, is_my_turn):
        # 캐시 키 생성
        board_key = board_to_key(current_board)
        cache_key = (x, y, ox, oy, board_key, is_my_turn)
        
        # 이미 계산된 상태면 캐시에서 반환
        if cache_key in cache:
            return cache[cache_key]
        
        # 현재 위치가 발판이 없는 경우 (이미 사라진 경우)
        if current_board[x][y] == 0:
            return (False, 0)
        
        # 이동 가능한 방향 확인
        can_move = False
        # 승리/패배 시 턴 수를 저장할 변수
        win_turns = float('inf')  # 승리 시 최소 턴
        lose_turns = 0  # 패배 시 최대 턴
        
        # 가능한 모든 방향 탐색
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            
            # 보드 범위 내이고 발판이 있는 경우
            if 0 <= nx < rows and 0 <= ny < cols and current_board[nx][ny] == 1:
                can_move = True
                
                # 현재 발판을 사라지게 함
                new_board = [row[:] for row in current_board]
                new_board[x][y] = 0
                
                # 상대 턴에서의 결과 확인
                # 현재 턴이 내 턴이었으면 다음은 상대 턴, 그 반대도 마찬가지
                opponent_result, opponent_turns = dfs(ox, oy, nx, ny, new_board, not is_my_turn)
                
                # 상대가 패배하면 나는 승리
                if not opponent_result:
                    win_turns = min(win_turns, opponent_turns + 1)  # 최소 턴 수로 승리
                else:
                    lose_turns = max(lose_turns, opponent_turns + 1)  # 최대 턴 수로 패배
        
        # 이동할 수 없는 경우 현재 플레이어 패배
        if not can_move:
            cache[cache_key] = (False, 0)
            return (False, 0)
        
        # 이길 수 있으면 최소 턴으로 승리
        if win_turns != float('inf'):
            cache[cache_key] = (True, win_turns)
            return (True, win_turns)
        # 질 수밖에 없으면 최대 턴으로 패배
        else:
            cache[cache_key] = (False, lose_turns)
            return (False, lose_turns)
    
    # A 플레이어부터 시작
    _, turns = dfs(aloc[0], aloc[1], bloc[0], bloc[1], board, True)
    
    # 총 이동 횟수 반환
    return turns
