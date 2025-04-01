import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        df.dt = pd.to_datetime(df.dt)
        return (
            df.set_index(["dt", "user"])
            .unstack(fill_value=0)
            .asfreq("D", fill_value=0)
            .stack()
            .sort_index(level=1)
            .reset_index()
        )

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "user": ["a", "a", "b", "b"],
                    "dt": ["2016-01-01", "2016-01-02", "2016-01-05", "2016-01-06"],
                    "val": [1, 33, 2, 1],
                }
            )
            df["dt"] = pd.to_datetime(df["dt"])
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "user": ["c", "c", "d", "d"],
                    "dt": ["2016-02-01", "2016-02-02", "2016-02-05", "2016-02-06"],
                    "val": [1, 33, 2, 1],
                }
            )
            df["dt"] = pd.to_datetime(df["dt"])
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

code = "\nuser_date_range = df.groupby('user')['dt'].agg(['min', 'max'])\nnew_index = []\nfor user, row in user_date_range.iterrows():\n    new_index.extend(pd.date_range(row['min'], row['max'], name='dt'))\nnew_df = pd.DataFrame(new_index, columns=['dt'])\nnew_df['user'] = new_df.groupby(new_df['dt'].dt.year).apply(lambda x: [user] * len(x)).explode().values\nresult = pd.merge(new_df, df, on=['user', 'dt'], how='left').sort_values(by=['dt', 'user']).fillna(0)\n"
test_execution(code)

