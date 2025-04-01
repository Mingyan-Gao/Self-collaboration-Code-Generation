import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        total_len = len(df)
        zero_len = (df["Column_x"] == 0).sum()
        idx = df["Column_x"].index[df["Column_x"].isnull()]
        total_nan_len = len(idx)
        first_nan = (total_len // 2) - zero_len
        df.loc[idx[0:first_nan], "Column_x"] = 0
        df.loc[idx[first_nan:total_nan_len], "Column_x"] = 1
        return df

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "Column_x": [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                    ]
                }
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "Column_x": [
                        0,
                        0,
                        0,
                        0,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                    ]
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

code = "\nnan_count = df['Column_x'].isnull().sum()\nnum_zeros = nan_count // 2\nnum_ones = nan_count - num_zeros\nfill_array = np.concatenate([np.zeros(num_zeros), np.ones(num_ones)])\ndf['Column_x'] = df['Column_x'].fillna(pd.Series(fill_array, index=df.index[df['Column_x'].isnull()]))\n"
test_execution(code)

