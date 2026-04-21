import json

# json파일 포멧팅(가독성 향상)

def format_matrix(matrix):
    return "[\n  " + ",\n  ".join(
        "[" + ", ".join(map(str, row)) + "]" for row in matrix
    ) + "\n]"

def recursive_format(obj):
    if isinstance(obj, list):
        # 2차원 배열이면 우리가 원하는 형식으로
        if all(isinstance(i, list) for i in obj):
            return format_matrix(obj)
        return [recursive_format(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: recursive_format(v) for k, v in obj.items()}
    return obj


with open("data.json") as f:
    data = json.load(f)

formatted = recursive_format(data)

# 문자열로 다시 출력
def stringify(obj, indent=0):
    space = "  " * indent
    if isinstance(obj, dict):
        items = []
        for k, v in obj.items():
            items.append(f'{space}  "{k}": {stringify(v, indent+1)}')
        return "{\n" + ",\n".join(items) + f"\n{space}" + "}"
    elif isinstance(obj, list):
        return json.dumps(obj)
    elif isinstance(obj, str) and obj.startswith("[\n"):
        return obj
    else:
        return json.dumps(obj)

result = stringify(formatted)

with open("data.json", "w") as f:
    f.write(result)

print("변환 완료: data.json")