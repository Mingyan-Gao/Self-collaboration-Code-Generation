import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        cols = list(df)[1:]
        cols = cols[::-1]
        for idx in df.index:
            s = 0
            cnt = 0
            for col in cols:
                if df.loc[idx, col] != 0:
                    cnt = min(cnt + 1, 2)
                    s = (s + df.loc[idx, col]) / cnt
                df.loc[idx, col] = s
        return df

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "Name": ["Name1", "Name2", "Name3"],
                    "2001": [2, 1, 0],
                    "2002": [5, 4, 5],
                    "2003": [0, 2, 0],
                    "2004": [0, 0, 0],
                    "2005": [4, 4, 0],
                    "2006": [6, 0, 2],
                }
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "Name": ["Name1", "Name2", "Name3"],
                    "2011": [2, 1, 0],
                    "2012": [5, 4, 5],
                    "2013": [0, 2, 0],
                    "2014": [0, 0, 0],
                    "2015": [4, 4, 0],
                    "2016": [6, 0, 2],
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

code = '\n    df1 = df.copy()\n    cols = df1.columns[1:]\n    for index, row in df1.iterrows():\n        running_sum = 0\n        running_count = 0\n        for col in reversed(cols):\n            if row[col] != 0:\n                running_sum += row[col]\n                running_count += 1\n            if running_count > 0:\n                df1.loc[index, col] = running_sum / running_count\n            else:\n                df1.loc[index, col] = 0\n    df = df1\n'
test_execution(code)

