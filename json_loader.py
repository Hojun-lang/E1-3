import json


def load_json_file(file_path: str) -> dict:
    """
    JSON 파일을 읽어서 파이썬 딕셔너리로 반환하는 함수.

    역할:
    1. 주어진 경로의 JSON 파일을 연다.
    2. JSON 내용을 파이썬 dict로 변환한다.
    3. 파일이 없거나 JSON 형식이 잘못되면 예외를 발생시킨다.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def extract_filters_and_patterns(data: dict) -> tuple[dict, dict]:
    """
    JSON 최상위 구조에서 filters와 patterns를 꺼내는 함수.

    역할:
    1. data 안에 filters 키가 있는지 확인한다.
    2. data 안에 patterns 키가 있는지 확인한다.
    3. 둘 다 있으면 반환한다.
    4. 없으면 ValueError를 발생시킨다.
    """
    if "filters" not in data:
        raise ValueError("JSON 스키마 오류: 'filters' 키가 없습니다.")

    if "patterns" not in data:
        raise ValueError("JSON 스키마 오류: 'patterns' 키가 없습니다.")

    filters = data["filters"]
    patterns = data["patterns"]

    if not isinstance(filters, dict):
        raise ValueError("JSON 스키마 오류: 'filters'는 객체(dict)여야 합니다.")

    if not isinstance(patterns, dict):
        raise ValueError("JSON 스키마 오류: 'patterns'는 객체(dict)여야 합니다.")

    return filters, patterns

def normalize_label(raw_label: str) -> str:
    """
    다양한 라벨 표현을 프로그램 내부의 표준 라벨로 바꾸는 함수.

    표준 라벨:
    - "Cross"
    - "X"

    변환 규칙:
    - "+" -> "Cross"
    - "cross" -> "Cross"
    - "x" -> "X"

    지원하지 않는 값이 들어오면 ValueError를 발생시킨다.
    """
    cleaned_label = raw_label.strip().lower()

    if cleaned_label == "+":
        return "Cross"
    if cleaned_label == "cross":
        return "Cross"
    if cleaned_label == "x":
        return "X"

    raise ValueError(f"라벨 정규화 오류: 지원하지 않는 라벨입니다 -> {raw_label}")

def extract_size_from_pattern_key(pattern_key: str) -> int:
    """
    패턴 키에서 크기 숫자를 추출하는 함수.

    예:
    - "size_5_0" -> 5
    - "size_13_1" -> 13

    형식이 맞지 않으면 ValueError를 발생시킨다.
    """
    parts = pattern_key.split("_")

    # 기대 형식: size / 숫자 / 인덱스
    if len(parts) != 3:
        raise ValueError(f"패턴 키 형식 오류: {pattern_key}")

    if parts[0] != "size":
        raise ValueError(f"패턴 키 형식 오류: {pattern_key}")

    try:
        size = int(parts[1])
    except ValueError:
        raise ValueError(f"패턴 키 크기 추출 오류: {pattern_key}")

    return size

def get_filters_for_size(filters: dict, size: int) -> tuple[list[list[float]], list[list[float]]]:
    """
    주어진 크기에 맞는 Cross 필터와 X 필터를 가져오는 함수.

    예:
    size=5 이면 filters["size_5"] 안에서
    - cross 필터
    - x 필터
    를 꺼내고, 둘 다 표준 이름 기준으로 반환한다.

    반환값:
    - cross_filter
    - x_filter
    """
    size_key = f"size_{size}"

    if size_key not in filters:
        raise ValueError(f"필터 조회 오류: '{size_key}' 필터가 없습니다.")

    size_filter_group = filters[size_key]

    if "cross" not in size_filter_group:
        raise ValueError(f"필터 조회 오류: '{size_key}'에 cross 필터가 없습니다.")

    if "x" not in size_filter_group:
        raise ValueError(f"필터 조회 오류: '{size_key}'에 x 필터가 없습니다.")

    cross_filter = size_filter_group["cross"]
    x_filter = size_filter_group["x"]

    return cross_filter, x_filter

def validate_matrix_size(matrix: list[list[float]], expected_size: int) -> None:
    """
    행렬의 크기가 expected_size x expected_size인지 검증하는 함수.

    역할:
    1. 행 개수가 맞는지 검사
    2. 각 행의 열 개수가 맞는지 검사
    3. 하나라도 틀리면 ValueError 발생

    예:
    expected_size=5인데 4x4면 오류 발생
    """
    if len(matrix) != expected_size:
        raise ValueError(f"크기 불일치: 행 개수 {len(matrix)} != {expected_size}")

    for row in matrix:
        if len(row) != expected_size:
            raise ValueError(f"크기 불일치: 열 개수 {len(row)} != {expected_size}")