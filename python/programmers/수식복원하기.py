def solution(expressions):
    # 입력값에서 최소 진법 힌트 얻기
    min_base = find_min_base(expressions)
    
    # 결과값이 X가 아닌 수식들을 통해 가능한 진법 찾기
    possible_bases = find_possible_bases(expressions, min_base)
    
    # 결과값이 X인 수식들의 결과 계산
    results = []
    for expr in expressions:
        if 'X' in expr:
            result = calculate_result(expr, possible_bases)
            results.append(result)
    
    return results

def find_min_base(expressions):
    # 수식에 등장하는 가장 큰 숫자를 찾아 최소 진법 결정
    max_digit = 0
    for expr in expressions:
        parts = expr.split(' ')
        for part in parts:
            if part != '+' and part != '-' and part != '=' and part != 'X':
                for digit in part:
                    if digit.isdigit() and int(digit) > max_digit:
                        max_digit = int(digit)
    
    # 최소 진법은 가장 큰 숫자 + 1
    return max_digit + 1

def find_possible_bases(expressions, min_base):
    # 각 진법별로 모든 수식이 성립하는지 확인
    valid_bases = []
    
    # min_base부터 9진법까지 검사
    for base in range(min_base, 10):
        valid = True
        for expr in expressions:
            if 'X' not in expr and not is_valid_expression(expr, base):
                valid = False
                break
        
        if valid:
            valid_bases.append(base)
    
    return valid_bases

def is_valid_expression(expr, base):
    # 수식 파싱
    parts = expr.split(' ')
    a_str = parts[0]
    op = parts[1]
    b_str = parts[2]
    c_str = parts[4]
    
    # 해당 진법에서 유효한 숫자인지 확인
    if not is_valid_in_base(a_str, base) or not is_valid_in_base(b_str, base):
        return False
    
    if c_str != 'X' and not is_valid_in_base(c_str, base):
        return False
    
    # 10진수로 변환
    a = convert_from_base(a_str, base)
    b = convert_from_base(b_str, base)
    
    if c_str == 'X':
        return True  # X는 결과를 모르므로 항상 유효
    
    c = convert_from_base(c_str, base)
    
    # 수식 검증
    if op == '+':
        return a + b == c
    else:  # op == '-'
        return a - b == c

def is_valid_in_base(num_str, base):
    # 해당 진법에서 유효한 숫자인지 확인
    for digit in num_str:
        if not digit.isdigit() or int(digit) >= base:
            return False
    return True

def convert_from_base(num_str, base):
    # 해당 진법의 숫자를 10진수로 변환
    result = 0
    for digit in num_str:
        result = result * base + int(digit)
    return result

def convert_to_base(num, base):
    # 10진수를 해당 진법으로 변환
    if num == 0:
        return '0'
    
    digits = []
    while num > 0:
        digits.append(str(num % base))
        num //= base
    
    return ''.join(reversed(digits))

def calculate_result(expr, possible_bases):
    # 수식 파싱
    parts = expr.split(' ')
    a_str = parts[0]
    op = parts[1]
    b_str = parts[2]
    
    # 가능한 모든 진법에 대해 결과 계산
    results = {}
    
    # 각 진법별로 결과 계산
    for base in possible_bases:
        # 해당 진법에서 유효한 숫자인지 확인
        if not is_valid_in_base(a_str, base) or not is_valid_in_base(b_str, base):
            continue
            
        # 10진수로 변환
        a = convert_from_base(a_str, base)
        b = convert_from_base(b_str, base)
        
        # 결과 계산
        if op == '+':
            result = a + b
        else:  # op == '-'
            result = a - b
        
        # 결과를 해당 진법으로 변환
        result_in_base = convert_to_base(result, base)
        
        # 결과가 해당 진법에서 유효한지 확인
        if is_valid_in_base(result_in_base, base):
            # 결과를 저장
            if result_in_base in results:
                results[result_in_base].append(base)
            else:
                results[result_in_base] = [base]
    
    # 결과 분석
    if len(results) == 0:
        # 가능한 결과가 없는 경우 (이론적으로는 발생하지 않아야 함)
        return parts[0] + ' ' + parts[1] + ' ' + parts[2] + ' = ?'
    elif len(results) == 1:
        # 모든 진법에서 결과가 같은 경우
        result_value = list(results.keys())[0]
        return parts[0] + ' ' + parts[1] + ' ' + parts[2] + ' = ' + result_value
    else:
        # 진법에 따라 결과가 다른 경우
        return parts[0] + ' ' + parts[1] + ' ' + parts[2] + ' = ?'
