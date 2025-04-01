import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return (
            df.set_index(["user", "01/12/15"])
            .stack()
            .reset_index(name="value")
            .rename(columns={"level_2": "others"})
        )

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "user": ["u1", "u2", "u3"],
                    "01/12/15": [100, 200, -50],
                    "02/12/15": [300, -100, 200],
                    "someBool": [True, False, True],
                }
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "user": ["u1", "u2", "u3"],
                    "01/12/15": [300, -100, 200],
                    "02/12/15": [100, 200, -50],
                    "someBool": [True, False, True],
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
result = df
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\ndf = pd.melt(df, id_vars=['user', '01/12/15'], value_vars=['02/12/15', 'someBool'], var_name='others', value_name='value')\ndf = df[['user', '01/12/15', 'others', 'value']]\n"
test_execution(code)

