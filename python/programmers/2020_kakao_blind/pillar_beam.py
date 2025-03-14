def solution(n, build_frame):
    # 설치된 구조물을 저장할 집합
    structures = set()
    
    # 기둥 설치 가능 여부 확인
    def can_build_pillar(x, y):
        # 바닥 위에 있는 경우
        if y == 0:
            return True
        # 보의 한쪽 끝 부분 위에 있는 경우
        if (x-1, y, 1) in structures or (x, y, 1) in structures:
            return True
        # 다른 기둥 위에 있는 경우
        if (x, y-1, 0) in structures:
            return True
        return False
    
    # 보 설치 가능 여부 확인
    def can_build_beam(x, y):
        # 한쪽 끝 부분이 기둥 위에 있는 경우
        if (x, y-1, 0) in structures or (x+1, y-1, 0) in structures:
            return True
        # 양쪽 끝 부분이 다른 보와 연결되어 있는 경우
        if (x-1, y, 1) in structures and (x+1, y, 1) in structures:
            return True
        return False
    
    # 구조물 삭제 가능 여부 확인
    def can_delete(x, y, a):
        # 일단 구조물 삭제
        structures.remove((x, y, a))
        
        # 삭제 후 남은 구조물들이 규칙을 만족하는지 확인
        valid = True
        
        # 모든 구조물을 순회하며 규칙 검증
        for struct_x, struct_y, struct_a in structures:
            # 기둥인 경우
            if struct_a == 0:
                if not can_build_pillar(struct_x, struct_y):
                    valid = False
                    break
            # 보인 경우
            else:
                if not can_build_beam(struct_x, struct_y):
                    valid = False
                    break
        
        # 검증 실패 시 삭제했던 구조물 복구
        if not valid:
            structures.add((x, y, a))
            
        return valid
    
    # 주어진 작업 순서대로 실행
    for x, y, a, b in build_frame:
        # 설치 작업
        if b == 1:
            if a == 0:  # 기둥 설치
                if can_build_pillar(x, y):
                    structures.add((x, y, a))
            else:  # 보 설치
                if can_build_beam(x, y):
                    structures.add((x, y, a))
        # 삭제 작업
        else:
            if (x, y, a) in structures:
                if can_delete(x, y, a):
                    pass  # 이미 can_delete 함수에서 삭제 완료
                else:
                    structures.add((x, y, a))  # 삭제 불가능하므로 다시 추가
    
    # 결과 정렬 및 반환
    answer = sorted(list(structures), key=lambda x: (x[0], x[1], x[2]))
    # 튜플 형태의 원소를 리스트 형태로 변환
    return [[x, y, a] for x, y, a in answer]

# 테스트 코드
if __name__ == "__main__":
    # 테스트 케이스 1
    n1 = 5
    build_frame1 = [[1, 0, 0, 1], [1, 1, 1, 1], [2, 1, 0, 1], [2, 2, 1, 1], [5, 0, 0, 1], [5, 1, 0, 1], [4, 2, 1, 1], [3, 2, 1, 1]]
    expected1 = [[1, 0, 0], [1, 1, 1], [2, 1, 0], [2, 2, 1], [3, 2, 1], [4, 2, 1], [5, 0, 0], [5, 1, 0]]
    result1 = solution(n1, build_frame1)
    print("테스트 케이스 1:", result1)
    print("예상 결과:", expected1)
    print("정답 여부:", result1 == expected1)
    
    # 테스트 케이스 2
    n2 = 5
    build_frame2 = [[0, 0, 0, 1], [2, 0, 0, 1], [4, 0, 0, 1], [0, 1, 1, 1], [1, 1, 1, 1], [2, 1, 1, 1], [3, 1, 1, 1], [2, 0, 0, 0], [1, 1, 1, 0], [2, 2, 0, 1]]
    expected2 = [[0, 0, 0], [0, 1, 1], [1, 1, 1], [2, 1, 1], [3, 1, 1], [4, 0, 0]]
    result2 = solution(n2, build_frame2)
    print("\n테스트 케이스 2:", result2)
    print("예상 결과:", expected2)
    print("정답 여부:", result2 == expected2)
