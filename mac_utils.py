import time

# 패턴과 필터의 MAC(Multiply-Accumulate) 점수를 계산하는 함수.
def calculate_mac(pattern: list[list[float]], filter_matrix: list[list[float]]) -> float:

    total = 0.0

    # 바깥 반복문: 행(row)을 하나씩 돈다
    for row_index in range(len(pattern)):
        # 안쪽 반복문: 각 행의 열(column)을 하나씩 돈다
        for col_index in range(len(pattern[row_index])):
            multiplied_value = pattern[row_index][col_index] * filter_matrix[row_index][col_index]
            total += multiplied_value

    return total

# 두 점수를 비교해서 판정 결과를 반환하는 함수.
def decide_winner(score_a: float, score_b: float, epsilon: float = 1e-9) -> str:

    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"
        
# MAC 연산의 평균 실행 시간을 ms 단위로 측정하는 함수.
def measure_average_mac_time(pattern: list[list[float]], filter_matrix: list[list[float]], repeat: int = 10) -> float:

    total_elapsed_ms = 0.0

    for _ in range(repeat):
        start_time = time.perf_counter()
        calculate_mac(pattern, filter_matrix)
        end_time = time.perf_counter()

        elapsed_ms = (end_time - start_time) * 1000
        total_elapsed_ms += elapsed_ms

    return total_elapsed_ms / repeat

# 하나의 패턴에 대해 여러 필터와의 MAC 연산 전체 시간을 측정하는 함수.
def measure_average_multi_mac_time(
    pattern: list[list[float]],
    filters: list[list[list[float]]],
    repeat: int = 10
) -> float:
    total_elapsed_ms = 0.0

    for _ in range(repeat):
        start_time = time.perf_counter()

        for filter_matrix in filters:
            calculate_mac(pattern, filter_matrix)

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000
        total_elapsed_ms += elapsed_ms

    return total_elapsed_ms / repeat