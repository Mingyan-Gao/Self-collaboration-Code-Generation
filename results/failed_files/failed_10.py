import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        if len(df.columns) == 1:
            if df.values.size == 1:
                return df.values[0][0]
            return df.values.squeeze()
        grouped = df.groupby(df.columns[0])
        d = {k: generate_ans(t.iloc[:, 1:]) for k, t in grouped}
        return d

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "name": ["A", "A", "B", "C", "B", "A"],
                    "v1": ["A1", "A2", "B1", "C1", "B2", "A2"],
                    "v2": ["A11", "A12", "B12", "C11", "B21", "A21"],
                    "v3": [1, 2, 3, 4, 5, 6],
                }
            )
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        assert result == ans
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
df = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\nresult = {}\nfor name in df['name'].unique():\n    result[name] = {}\n    sub_df = df[df['name'] == name]\n    for _, row in sub_df.iterrows():\n        current_dict = result[name]\n        for col in df.columns[1:-1]:\n            value = row[col]\n            if value not in current_dict:\n                current_dict[value] = {}\n            current_dict = current_dict[value]\n        last_col = df.columns[-1]\n        current_dict[row[last_col]] = row[last_col]\ndef merge_dicts(dict1, dict2):\n    for key, value in dict2.items():\n        if key in dict1:\n            if isinstance(value, dict) and isinstance(dict1[key], dict):\n                merge_dicts(dict1[key], value)\n            else:\n                if not isinstance(dict1[key], list):\n                    dict1[key] = [dict1[key]]\n                dict1[key].append(value)\n        else:\n            dict1[key] = value\n    return dict1\nresult = {}\nfor name in df['name'].unique():\n    result[name] = {}\n    sub_df = df[df['name'] == name]\n    for _, row in sub_df.iterrows():\n        current_dict = result[name]\n        for col in df.columns[1:-1]:\n            value = row[col]\n            if col == df.columns[-2]:\n                last_dict = current_dict\n                last_value = value\n                if value not in current_dict:\n                    current_dict[value] = {}\n                current_dict = current_dict[value]\n            else:\n                if value not in current_dict:\n                    current_dict[value] = {}\n                current_dict = current_dict[value]\n        last_col = df.columns[-1]\n        current_dict[row[last_col]] = row[last_col]\nimport collections\ndef build_nested_dict(df):\n    output = collections.defaultdict(lambda: collections.defaultdict(dict))\n    for index, row in df.iterrows():\n        d = output[row['name']]\n        for i, col in enumerate(df.columns[1:-1]):\n            if not isinstance(d, dict):\n                break\n            d = d.setdefault(row[col], {})\n        if isinstance(d, dict):\n            d[row[df.columns[-1]]] = row[df.columns[-1]]\n    return output\nresult = build_nested_dict(df)\nfrom collections import defaultdict\ndef to_nested_dict(df):\n    result = defaultdict(lambda: defaultdict(dict))\n    for _, row in df.iterrows():\n        current_level = result[row['name']]\n        for col in df.columns[1:-1]:\n            current_level = current_level[row[col]]\n        current_level[row[df.columns[-1]]] = row[df.columns[-1]]\n    return {k: {k2: dict(v2) for k2, v2 in v.items()} for k, v in result.items()}\nresult = to_nested_dict(df)\n"
test_execution(code)

