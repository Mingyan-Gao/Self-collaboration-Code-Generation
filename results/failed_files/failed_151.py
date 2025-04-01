import pandas as pd
import numpy as np
from itertools import product
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data

        def get_relation(df, col1, col2):
            first_max = df[[col1, col2]].groupby(col1).count().max()[0]
            second_max = df[[col1, col2]].groupby(col2).count().max()[0]
            if first_max == 1:
                if second_max == 1:
                    return "one-to-one"
                else:
                    return "one-to-many"
            else:
                if second_max == 1:
                    return "many-to-one"
                else:
                    return "many-to-many"

        result = []
        for col_i, col_j in product(df.columns, df.columns):
            if col_i == col_j:
                continue
            result.append(col_i + " " + col_j + " " + get_relation(df, col_i, col_j))
        return result

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "Column1": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "Column2": [4, 3, 6, 8, 3, 4, 1, 4, 3],
                    "Column3": [7, 3, 3, 1, 2, 2, 3, 2, 7],
                    "Column4": [9, 8, 7, 6, 5, 4, 3, 2, 1],
                    "Column5": [1, 1, 1, 1, 1, 1, 1, 1, 1],
                }
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "Column1": [4, 3, 6, 8, 3, 4, 1, 4, 3],
                    "Column2": [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    "Column3": [7, 3, 3, 1, 2, 2, 3, 2, 7],
                    "Column4": [9, 8, 7, 6, 5, 4, 3, 2, 1],
                    "Column5": [1, 2, 3, 4, 5, 6, 7, 8, 9],
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
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport pandas as pd\n\ndf = pd.DataFrame({\n    \'Column1\': [1, 2, 3, 4, 5, 6, 7, 8, 9],\n    \'Column2\': [4, 3, 6, 8, 3, 4, 1, 4, 3],\n    \'Column3\': [7, 3, 3, 1, 2, 2, 3, 2, 7],\n    \'Column4\': [9, 8, 7, 6, 5, 4, 3, 2, 1],\n    \'Column5\': [1, 1, 1, 1, 1, 1, 1, 1, 1]})\n\ndef determine_relationship(df, col_a, col_b):\n    unique_a = df[col_a].nunique()\n    unique_b = df[col_b].nunique()\n    unique_pairs = df.groupby([col_a, col_b]).size().reset_index().shape[0]\n\n    if unique_a == unique_b == unique_pairs:\n        return "one-to-one"\n    elif unique_a == unique_pairs and unique_a < unique_b:\n        return "one-to-many"\n    elif unique_b == unique_pairs and unique_b < unique_a:\n        return "many-to-one"\n    else:\n        return "many-to-many"\n\nresults = []\ncolumns = df.columns\n\nfor col_a in columns:\n    for col_b in columns:\n        if col_a != col_b:\n            relationship = determine_relationship(df, col_a, col_b)\n            results.append(f"{col_a} {col_b} {relationship}")\n'
test_execution(code)

