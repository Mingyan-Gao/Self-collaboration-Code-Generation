import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        df["frequent"] = df.mode(axis=1)
        for i in df.index:
            df.loc[i, "freq_count"] = (df.iloc[i] == df.loc[i, "frequent"]).sum() - 1
        return df

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "bit1": [0, 1, 1],
                    "bit2": [0, 1, 0],
                    "bit3": [1, 0, 1],
                    "bit4": [1, 0, 1],
                    "bit5": [0, 1, 1],
                }
            )
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        pd.testing.assert_frame_equal(result, ans)
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
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\ndef most_frequent(row):\n    return row.value_counts().index[0], row.value_counts().iloc[0]\n\ndf['frequent'], df['freq_count'] = zip(*df.apply(most_frequent, axis=1))\n"
test_execution(code)

