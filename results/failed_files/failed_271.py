import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        df["dogs"] = df["dogs"].apply(lambda x: round(x, 2) if str(x) != "<NA>" else x)
        return df

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                [
                    (0.21, 0.3212),
                    (0.01, 0.61237),
                    (0.66123, 0.03),
                    (0.21, 0.18),
                    (pd.NA, 0.18),
                ],
                columns=["dogs", "cats"],
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                [
                    (0.215, 0.3212),
                    (0.01, 0.11237),
                    (0.36123, 0.03),
                    (0.21, 0.18),
                    (pd.NA, 0.18),
                ],
                columns=["dogs", "cats"],
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

code = "\nimport numpy as np\ndf['dogs'] = df['dogs'].fillna(np.nan).round(2)\n"
test_execution(code)

