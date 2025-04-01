import numpy as np
import pandas as pd
import itertools as IT
import copy
import scipy.stats as stats


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                [[1, 5, 2], [2, 4, 4], [3, 3, 1], [4, 2, 2], [5, 1, 4]],
                columns=["A", "B", "C"],
                index=[1, 2, 3, 4, 5],
            )
        elif test_case_id == 2:
            df = pd.DataFrame(
                [[1, 3, 2], [2, 5, 4], [2, 3, 1], [1, 2, 2], [5, 8, 4]],
                columns=["A", "B", "C"],
                index=[1, 2, 3, 4, 5],
            )
        return df

    def generate_ans(data):
        _a = data
        df = _a
        for col1, col2 in IT.combinations(df.columns, 2):

            def tau(idx):
                B = df[[col1, col2]].iloc[idx]
                return stats.kendalltau(B[col1], B[col2])[0]

            df[col1 + col2] = (
                pd.Series(np.arange(len(df)), index=df.index).rolling(3).apply(tau)
            )
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    pd.testing.assert_frame_equal(result, ans, atol=1e-3, check_dtype=False)
    return 1


exec_context = r"""
import pandas as pd
import numpy as np
import scipy.stats as stats
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

code = "\nimport pandas as pd\nimport numpy as np\nimport scipy.stats as stats\nfrom itertools import combinations\n\ndf = pd.DataFrame([[1, 5, 2], [2, 4, 4], [3, 3, 1], [4, 2, 2], [5, 1, 4]], \n                 columns=['A', 'B', 'C'], index = [1, 2, 3, 4, 5])\n\ndef kendall_tau_rolling(df, col1, col2, window):\n    def calculate_kendalltau(x):\n        if len(x[col1]) < window:\n            return np.nan\n        else:\n            return stats.kendalltau(x[col1], x[col2])[0]\n    return df[[col1, col2]].rolling(window=window).apply(calculate_kendalltau, raw=False)\n\nwindow = 3\ncolumn_pairs = list(combinations(df.columns, 2))\n\nfor col1, col2 in column_pairs:\n    df[col1 + col2] = kendall_tau_rolling(df, col1, col2, window)\n"
test_execution(code)

