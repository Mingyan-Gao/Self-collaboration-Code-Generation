import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return df.loc[(df.sum(axis=1) != 0), (df.sum(axis=0) != 0)]

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                [
                    [-1, -1, 0, 2],
                    [0, 0, 0, 0],
                    [1, 0, 0, 1],
                    [0, 1, 0, 0],
                    [1, 1, 0, 1],
                ],
                columns=["A", "B", "C", "D"],
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                [[1, 1, 0, 1], [0, 0, 0, 0], [1, 0, 0, 1], [0, 1, 0, 0], [1, 1, 0, 1]],
                columns=["A", "B", "C", "D"],
            )
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        pd.testing.assert_frame_equal(result, ans, check_dtype=False)
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

code = '\n    row_sums = df.sum(axis=1)\n    col_sums = df.sum(axis=0)\n    rows_to_keep = row_sums != 0\n    cols_to_keep = col_sums != 0\n    result = df.loc[rows_to_keep, cols_to_keep]\n'
test_execution(code)

