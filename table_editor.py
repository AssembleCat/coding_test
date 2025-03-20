class Cell:
    def __init__(self):
        self.value = ""
        self.group = None

class TableEditor:
    def __init__(self):
        self.size = 50
        self.table = [[Cell() for _ in range(self.size + 1)] for _ in range(self.size + 1)]
        self.value_cells = {}  # value to cells mapping
        self.group_counter = 0
        self.group_values = {}  # group to value mapping

    def find_group(self, r, c):
        cell = self.table[r][c]
        if cell.group is None:
            self.group_counter += 1
            cell.group = self.group_counter
        return cell.group

    def merge_groups(self, group1, group2):
        # 모든 셀의 그룹을 group1으로 변경
        for r in range(1, self.size + 1):
            for c in range(1, self.size + 1):
                if self.table[r][c].group == group2:
                    self.table[r][c].group = group1

    def update_cell(self, r, c, value):
        cell = self.table[r][c]
        old_value = cell.value
        
        # 이전 값 매핑에서 제거
        if old_value and old_value in self.value_cells:
            self.value_cells[old_value].remove((r, c))
            if not self.value_cells[old_value]:
                del self.value_cells[old_value]

        # 새 값 설정 및 매핑 추가
        cell.value = value
        if value:
            if value not in self.value_cells:
                self.value_cells[value] = set()
            self.value_cells[value].add((r, c))

        # 같은 그룹의 모든 셀 업데이트
        if cell.group:
            group = cell.group
            for i in range(1, self.size + 1):
                for j in range(1, self.size + 1):
                    if self.table[i][j].group == group:
                        self.update_cell_value(i, j, value)

    def update_cell_value(self, r, c, value):
        cell = self.table[r][c]
        old_value = cell.value
        
        # 이전 값 매핑에서 제거
        if old_value and old_value in self.value_cells:
            self.value_cells[old_value].remove((r, c))
            if not self.value_cells[old_value]:
                del self.value_cells[old_value]

        # 새 값 설정 및 매핑 추가
        cell.value = value
        if value:
            if value not in self.value_cells:
                self.value_cells[value] = set()
            self.value_cells[value].add((r, c))

    def update_value(self, value1, value2):
        if value1 not in self.value_cells:
            return
        
        # value1을 가진 모든 셀의 좌표를 저장
        cells_to_update = list(self.value_cells[value1])
        
        # 각 셀 업데이트
        for r, c in cells_to_update:
            self.update_cell(r, c, value2)

    def merge(self, r1, c1, r2, c2):
        if r1 == r2 and c1 == c2:
            return

        cell1, cell2 = self.table[r1][c1], self.table[r2][c2]
        group1 = self.find_group(r1, c1)
        group2 = self.find_group(r2, c2)

        if group1 != group2:
            # cell1의 값을 우선으로 사용
            value = cell1.value if cell1.value else cell2.value
            self.merge_groups(group1, group2)
            if value:
                self.update_cell(r1, c1, value)

    def unmerge(self, r, c):
        cell = self.table[r][c]
        if cell.group is None:
            return

        value = cell.value
        group = cell.group

        # 같은 그룹의 모든 셀 초기화
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.table[i][j].group == group:
                    self.table[i][j].group = None
                    self.update_cell(i, j, "")

        # 선택된 셀만 값 유지
        self.update_cell(r, c, value)

    def print_cell(self, r, c):
        return self.table[r][c].value if self.table[r][c].value else "EMPTY"

def solution(commands):
    editor = TableEditor()
    result = []
    
    for command in commands:
        cmd = command.split()
        
        if cmd[0] == "UPDATE":
            if len(cmd) == 4:
                editor.update_cell(int(cmd[1]), int(cmd[2]), cmd[3])
            else:
                editor.update_value(cmd[1], cmd[2])
        elif cmd[0] == "MERGE":
            editor.merge(int(cmd[1]), int(cmd[2]), int(cmd[3]), int(cmd[4]))
        elif cmd[0] == "UNMERGE":
            editor.unmerge(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == "PRINT":
            result.append(editor.print_cell(int(cmd[1]), int(cmd[2])))
            
    return result

# 테스트
if __name__ == "__main__":
    # 테스트 케이스 1
    commands1 = ["UPDATE 1 1 menu", "UPDATE 1 2 category", "UPDATE 2 1 bibimbap", 
                "UPDATE 2 2 korean", "UPDATE 2 3 rice", "UPDATE 3 1 ramyeon", 
                "UPDATE 3 2 korean", "UPDATE 3 3 noodle", "UPDATE 3 4 instant", 
                "UPDATE 4 1 pasta", "UPDATE 4 2 italian", "UPDATE 4 3 noodle", 
                "MERGE 1 2 1 3", "MERGE 1 3 1 4", "UPDATE korean hansik", 
                "UPDATE 1 3 group", "UNMERGE 1 4", "PRINT 1 3", "PRINT 1 4"]
    
    # 테스트 케이스 2
    commands2 = ["UPDATE 1 1 a", "UPDATE 1 2 b", "UPDATE 2 1 c", "UPDATE 2 2 d", 
                "MERGE 1 1 1 2", "MERGE 2 2 2 1", "MERGE 2 1 1 1", "PRINT 1 1", 
                "UNMERGE 2 2", "PRINT 1 1"]
    
    print("테스트 케이스 1 결과:", solution(commands1))
    print("테스트 케이스 2 결과:", solution(commands2))
