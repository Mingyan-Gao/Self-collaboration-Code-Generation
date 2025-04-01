import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        data = data
        df, bins = data
        groups = df.groupby(["username", pd.cut(df.views, bins)])
        return groups.size().unstack()

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "username": [
                        "john",
                        "john",
                        "john",
                        "john",
                        "jane",
                        "jane",
                        "jane",
                        "jane",
                    ],
                    "post_id": [1, 2, 3, 4, 7, 8, 9, 10],
                    "views": [3, 23, 44, 82, 5, 25, 46, 56],
                }
            )
            bins = [1, 10, 25, 50, 100]
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "username": [
                        "john",
                        "john",
                        "john",
                        "john",
                        "jane",
                        "jane",
                        "jane",
                        "jane",
                    ],
                    "post_id": [1, 2, 3, 4, 7, 8, 9, 10],
                    "views": [3, 23, 44, 82, 5, 25, 46, 56],
                }
            )
            bins = [1, 5, 25, 50, 100]
        return df, bins

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
df, bins = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\ndf['views_bin'] = pd.cut(df['views'], bins, right=True)\nresult = df.groupby(['username', 'views_bin']).size().unstack(fill_value=0)\nresult.columns = result.columns.astype(str)\n"
test_execution(code)

