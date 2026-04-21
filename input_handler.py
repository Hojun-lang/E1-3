# size x size 크기의 행렬을 사용자에게 입력받는 함수.
def read_matrix(matrix_name: str, size: int) -> list[list[float]]:
    """
    역할:
    1. 행렬 이름과 크기를 안내한다.
    2. 한 줄씩 입력받아 parse_number_row()로 검사한다.
    3. 잘못 입력하면 같은 줄을 다시 입력받게 한다.
    4. 모든 줄이 올바르면 2차원 리스트를 반환한다.

    예:
    [
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0]
    ]
    """
    print(f"{matrix_name} ({size}줄 입력, 각 줄 공백 구분)")

    matrix = []
    
    for row_index in range(size):
        while True:
            row_text = input(f"{row_index + 1}번째 줄 입력: ")

            try: 
                row = parse_number_row(row_text, size)
                matrix.append(row)
                break
            except ValueError as error:
                print (error)
                print("다시 입력하세요.")
    
    return matrix

# 사용자가 입력한 한 줄 문자열을 숫자 리스트로 변환하는 함수.
def parse_number_row(row_text: str, expected_size: int) -> list[float]:
    parts = row_text.strip().split()

    # 입력된 숫자 개수가 기대한 개수와 다르면 오류 발생
    if len(parts) != expected_size:
        raise ValueError(
            f"입력 형식 오류: 각 줄에 {expected_size}개의 숫자를 공백으로 구분해 입력하세요. ex) 1 0 1"
        )
    
    numbers = []
    
    for part in parts:
        try:
            number = float(part) # 문자열을 실수 형태로 변환
            numbers.append(number)
        except ValueError:
            # 숫자로 바꿀 수 없는 문자열이 들어오면 오류 발생
            raise ValueError("입력 형식 오류: 숫자만 입력할 수 있습니다.")
    
    return numbers