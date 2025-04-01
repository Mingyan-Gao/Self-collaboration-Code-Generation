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
                    s += df.loc[idx, col]
                    cnt += 1
                df.loc[idx, col] = s / (max(cnt, 1))
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

code = "\nyears = ['2006', '2005', '2004', '2003', '2002', '2001']\n\nfor index, row in df.iterrows():\n    sum_so_far = 0\n    count = 0\n    for year in years:\n        value = row[year]\n        if value != 0:\n            sum_so_far += value\n            count += 1\n        if count == 0:\n            avg = 0\n        else:\n            avg = sum_so_far / count\n        df.loc[index, year] = avg\n"
test_execution(code)

