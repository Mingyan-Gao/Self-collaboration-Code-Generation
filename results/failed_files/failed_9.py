import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return df.loc[(df["keep_if_dup"] == "Yes") | ~df["url"].duplicated(keep="last")]

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "url": [
                        "A.com",
                        "A.com",
                        "A.com",
                        "B.com",
                        "B.com",
                        "C.com",
                        "B.com",
                    ],
                    "keep_if_dup": ["Yes", "Yes", "No", "No", "No", "No", "Yes"],
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
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\nkeep_mask = df['keep_if_dup'] == 'Yes'\nkeep_df = df[keep_mask]\ndrop_df = df[~keep_mask]\ndrop_df = drop_df.drop_duplicates(subset='url', keep='last')\nresult = pd.concat([keep_df, drop_df]).sort_index()\n"
test_execution(code)

