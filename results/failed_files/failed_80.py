import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        l = []
        for i in range(2 * (len(df) // 5) + (len(df) % 5) // 3 + 1):
            l.append(0)
        for i in range(len(df)):
            idx = 2 * (i // 5) + (i % 5) // 3
            if i % 5 < 3:
                l[idx] += df["col1"].iloc[i]
            elif i % 5 == 3:
                l[idx] = df["col1"].iloc[i]
            else:
                l[idx] = (l[idx] + df["col1"].iloc[i]) / 2
        return pd.DataFrame({"col1": l})

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame({"col1": [2, 1, 3, 1, 0, 2, 1, 3, 1]})
        if test_case_id == 2:
            df = pd.DataFrame({"col1": [1, 9, 2, 6, 0, 8, 1, 7, 1]})
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

code = "\nresults = []\ni = 0\nwhile i < len(df):\n    if i + 3 <= len(df):\n        results.append(df['col1'][i:i+3].sum())\n        i += 3\n    else:\n        results.append(df['col1'][i:i+2].mean())\n        i += 2\n    \nresult = pd.DataFrame({'col1': results})\n"
test_execution(code)

