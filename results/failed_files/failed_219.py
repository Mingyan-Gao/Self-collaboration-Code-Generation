import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return df.loc[df.groupby("item")["diff"].idxmin()]

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "item": [1, 1, 1, 2, 2, 2, 2, 3, 3],
                    "diff": [2, 1, 3, -1, 1, 4, -6, 0, 2],
                    "otherstuff": [1, 2, 7, 0, 3, 9, 2, 0, 9],
                }
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "item": [3, 3, 3, 1, 1, 1, 1, 2, 2],
                    "diff": [2, 1, 3, -1, 1, 4, -6, 0, 2],
                    "otherstuff": [1, 2, 7, 0, 3, 9, 2, 0, 9],
                }
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

code = '\nmin_diff = df.groupby("item")["diff"].min().reset_index()\ndf_min = pd.merge(df, min_diff, on="item", suffixes=("", "_min"))\nresult = df_min[df_min["diff"] == df_min["diff_min"]][["item", "diff", "otherstuff"]]\n'
test_execution(code)

