import json
from input_handler import read_matrix
from mac_utils import calculate_mac, decide_winner, measure_average_mac_time
from json_loader import load_json_file, extract_filters_and_patterns
from json_loader import (
    load_json_file,
    extract_filters_and_patterns,
    normalize_label,
    extract_size_from_pattern_key,
    get_filters_for_size,
    validate_matrix_size
)

# 메뉴 표시
def show_menu() -> str:
    print("=== Mini NPU Simulator ===")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    return input("선택: ").strip()

# 1번(사용자 입력 모드)
def user_input_mode() -> None:
    print("사용자 입력 모드를 선택했습니다.")
    print()

    filter_a = read_matrix("필터 A", 3)
    print()

    filter_b = read_matrix("필터 B", 3)
    print()

    pattern = read_matrix("패턴", 3)
    print()

    print("입력이 완료되었습니다.")
    print("필터 A:", filter_a)
    print("필터 B:", filter_b)
    print("패턴  :", pattern)

    score_a = calculate_mac(pattern, filter_a)
    score_b = calculate_mac(pattern, filter_b)
    result = decide_winner(score_a, score_b)
        
    avg_time_a = measure_average_mac_time(pattern, filter_a, repeat=10)
    avg_time_b = measure_average_mac_time(pattern, filter_b, repeat=10)

    """
    두 필터 각각의 평균 시간을 구한 뒤,
    사용자에게는 전체 연산 감각을 보기 쉽게 평균 하나로 보여준다.
    """
    avg_time_total = (avg_time_a + avg_time_b) / 2

    print("=== MAC 결과 ===")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"  판정: {result}")
    print(f"연산 시간(평균/10회): {avg_time_total:.6f} ms")

# 2번(data.json 분석 모드)
def json_mode() -> None:
    
    print("data.json 분석 모드를 선택했습니다.")
    print()

    total_count = 0
    pass_count = 0
    fail_cases = []

    try:
        data = load_json_file("data.json")
        filters, patterns = extract_filters_and_patterns(data)

        for pattern_key, pattern_info in patterns.items():
            print(f"--- {pattern_key} ---")
            total_count += 1

            try:
                # 1. size 추출
                size = extract_size_from_pattern_key(pattern_key)

                # 2. expected 정규화
                expected_raw = pattern_info["expected"]
                expected = normalize_label(expected_raw)

                # 3. input 가져오기
                pattern = pattern_info["input"]

                # 4. 필터 가져오기
                cross_filter, x_filter = get_filters_for_size(filters, size)

                # 5. 크기 검증 (🔥 중요)
                validate_matrix_size(pattern, size)
                validate_matrix_size(cross_filter, size)
                validate_matrix_size(x_filter, size)

                # 6. MAC 계산
                score_cross = calculate_mac(pattern, cross_filter)
                score_x = calculate_mac(pattern, x_filter)

                # 7. 판정
                result = decide_winner(score_cross, score_x)

                # A/B → Cross/X로 변환
                if result == "A":
                    result_label = "Cross"
                elif result == "B":
                    result_label = "X"
                else:
                    result_label = "UNDECIDED"

                # 8. PASS / FAIL 판단
                if result_label == expected:
                    print(f"Cross 점수: {score_cross}")
                    print(f"X 점수: {score_x}")
                    print(f"판정: {result_label} | expected: {expected} | PASS")
                    pass_count += 1
                else:
                    print(f"Cross 점수: {score_cross}")
                    print(f"X 점수: {score_x}")
                    print(f"판정: {result_label} | expected: {expected} | FAIL")

                    fail_cases.append(
                        f"{pattern_key}: expected={expected}, result={result_label}"
                    )

            except KeyError as error:
                print(f"스키마 오류: {error}")
                fail_cases.append(f"{pattern_key}: 스키마 오류")
            except ValueError as error:
                print(f"FAIL - {error}")
                fail_cases.append(f"{pattern_key}: {error}")

            print()

        # 🔥 결과 요약
        print("=== 결과 요약 ===")
        print(f"총 테스트: {total_count}")
        print(f"통과: {pass_count}")
        print(f"실패: {total_count - pass_count}")

        if fail_cases:
            print("실패 케이스:")
            for case in fail_cases:
                print("-", case)

    except FileNotFoundError:
        print("파일 오류: data.json 파일을 찾을 수 없습니다.")
    except json.JSONDecodeError:
        print("파일 오류: JSON 형식이 올바르지 않습니다.")
    except ValueError as error:
        print(error)

# 프로그램 시작점
def main() -> None:
    choice = show_menu()

    if choice == "1":
        user_input_mode()
    elif choice == "2":
        json_mode()
    else:
        print("잘못된 입력입니다. 1 또는 2를 입력하세요.")

if __name__ == "__main__":
    main()