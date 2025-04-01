import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        df.dt = pd.to_datetime(df.dt)
        result = (
            df.set_index(["dt", "user"])
            .unstack(fill_value=-11414)
            .asfreq("D", fill_value=-11414)
        )
        for col in result.columns:
            Max = result[col].max()
            for idx in result.index:
                if result.loc[idx, col] == -11414:
                    result.loc[idx, col] = Max
        return result.stack().sort_index(level=1).reset_index()

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

code = "\ndef expand_dates(group):\n    min_date = group['dt'].min()\n    max_date = group['dt'].max()\n    date_range = pd.date_range(min_date, max_date)\n    expanded_df = pd.DataFrame({'dt': date_range, 'user': group['user'].iloc[0]})\n    max_val = group['val'].max()\n    expanded_df['val'] = max_val\n    return expanded_df\n\ngrouped = df.groupby('user')\nresult = grouped.apply(expand_dates)\nresult = pd.concat(result).reset_index(drop=True)\nresult = result.sort_values(by=['user', 'dt']).reset_index(drop=True)\n"
test_execution(code)

