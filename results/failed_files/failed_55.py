import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return df.mask(~(df == df.min()).cumsum().astype(bool)).idxmax()

    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array(
                [
                    [1.0, 0.9, 1.0],
                    [0.9, 0.9, 1.0],
                    [0.8, 1.0, 0.5],
                    [1.0, 0.3, 0.2],
                    [1.0, 0.2, 0.1],
                    [0.9, 1.0, 1.0],
                    [1.0, 0.9, 1.0],
                    [0.6, 0.9, 0.7],
                    [1.0, 0.9, 0.8],
                    [1.0, 0.8, 0.9],
                ]
            )
            idx = pd.date_range("2017", periods=a.shape[0])
            df = pd.DataFrame(a, index=idx, columns=list("abc"))
        if test_case_id == 2:
            a = np.array(
                [
                    [1.0, 0.9, 1.0],
                    [0.9, 0.9, 1.0],
                    [0.8, 1.0, 0.5],
                    [1.0, 0.3, 0.2],
                    [1.0, 0.2, 0.1],
                    [0.9, 1.0, 1.0],
                    [0.9, 0.9, 1.0],
                    [0.6, 0.9, 0.7],
                    [1.0, 0.9, 0.8],
                    [1.0, 0.8, 0.9],
                ]
            )
            idx = pd.date_range("2022", periods=a.shape[0])
            df = pd.DataFrame(a, index=idx, columns=list("abc"))
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        pd.testing.assert_series_equal(result, ans, check_dtype=False)
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

code = '\n    min_indices = df.idxmin()\n\n    def find_max_after_min(column, min_index):\n        sliced_column = column[column.index >= min_index]\n        if sliced_column.empty:\n            return None\n        return sliced_column.idxmax()\n\n    result = df.apply(lambda col: find_max_after_min(col, min_indices[col.name]), axis=0)\n'
test_execution(code)

