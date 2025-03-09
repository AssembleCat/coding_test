from bisect import bisect_left
from itertools import combinations

def solution(info, query):
    answer = []
    info_dict = {}
    
    # 1. 정보를 파싱하여 모든 가능한 조합의 경우에 대한 점수 리스트 생성
    for i in info:
        i_split = i.split()
        conditions = i_split[:-1]  # 언어, 직군, 경력, 소울푸드
        score = int(i_split[-1])   # 점수
        
        # 해당 조건의 모든 부분 집합에 대해 점수 추가
        for j in range(5):  # 0, 1, 2, 3, 4개를 선택하는 경우
            for c in combinations(range(4), j):
                # 현재 조건에서 특정 위치를 '-'로 대체
                new_conditions = conditions.copy()
                for idx in c:
                    new_conditions[idx] = '-'
                
                key = ' '.join(new_conditions)
                if key in info_dict:
                    info_dict[key].append(score)
                else:
                    info_dict[key] = [score]
    
    # 2. 점수 리스트 정렬 (이진 탐색을 위해)
    for key in info_dict:
        info_dict[key].sort()
    
    # 3. 쿼리 처리
    for q in query:
        q = q.replace(" and ", " ")
        q_split = q.split()
        q_conditions = q_split[:-1]  # 조건
        q_score = int(q_split[-1])   # 점수
        
        key = ' '.join(q_conditions)
        
        # 해당 조건에 맞는 점수 리스트가 있는 경우
        if key in info_dict:
            scores = info_dict[key]
            # 이진 탐색으로 q_score 이상인 점수의 개수 찾기
            pos = bisect_left(scores, q_score)
            answer.append(len(scores) - pos)
        else:
            answer.append(0)
    
    return answer

# 테스트
if __name__ == "__main__":
    info = [
        "java backend junior pizza 150",
        "python frontend senior chicken 210",
        "python frontend senior chicken 150",
        "cpp backend senior pizza 260",
        "java backend junior chicken 80",
        "python backend senior chicken 50"
    ]
    query = [
        "java and backend and junior and pizza 100",
        "python and frontend and senior and chicken 200",
        "cpp and - and senior and pizza 250",
        "- and backend and senior and - 150",
        "- and - and - and chicken 100",
        "- and - and - and - 150"
    ]
    expected = [1, 1, 1, 1, 2, 4]
    
    result = solution(info, query)
    print(f"결과: {result}")
    print(f"예상: {expected}")
    print(f"정확성: {result == expected}")
