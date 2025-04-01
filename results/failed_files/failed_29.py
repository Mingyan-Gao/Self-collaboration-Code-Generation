import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        sh = 0
        min_R2 = 0
        for i in range(len(df)):
            min_R2 += (df["#1"].iloc[i] - df["#2"].iloc[i]) ** 2
        for i in range(len(df)):
            R2 = 0
            for j in range(len(df)):
                R2 += (df["#1"].iloc[j] - df["#2"].iloc[j]) ** 2
            if min_R2 > R2:
                sh = i
                min_R2 = R2
            df["#1"] = np.roll(df["#1"], shift=1)
        df["#1"] = np.roll(df["#1"], shift=sh)
        return df

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "#1": [11.6985, 43.6431, 54.9089, 63.1225, 72.4399],
                    "#2": [126.0, 134.0, 130.0, 126.0, 120.0],
                },
                index=[
                    "1980-01-01",
                    "1980-01-02",
                    "1980-01-03",
                    "1980-01-04",
                    "1980-01-05",
                ],
            )
        elif test_case_id == 2:
            df = pd.DataFrame(
                {"#1": [45, 51, 14, 11, 14], "#2": [126.0, 134.0, 130.0, 126.0, 120.0]},
                index=[
                    "1980-01-01",
                    "1980-01-02",
                    "1980-01-03",
                    "1980-01-04",
                    "1980-01-05",
                ],
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

code = "\nimport pandas as pd\nfrom scipy.stats import linregress\n\ndf = pd.DataFrame({'#1': [11.6985, 43.6431, 54.9089, 63.1225, 72.4399],\n                   '#2': [126.0, 134.0, 130.0, 126.0, 120.0]},\n                  index=['1980-01-01', '1980-01-02', '1980-01-03', '1980-01-04', '1980-01-05'])\n\ndef calculate_r_squared(col1, col2):\n    slope, intercept, r_value, p_value, std_err = linregress(col1, col2)\n    return r_value**2\n\ndef shift_column(df, column_name, shift):\n    shifted_column = df[column_name].shift(shift).fillna(df[column_name].iloc[-shift])\n    return shifted_column\n\nr_squared_values = []\nshifted_dataframes = []\n\nfor shift in range(1, len(df) + 1):\n    shifted_col1 = shift_column(df, '#1', shift)\n    r_squared = calculate_r_squared(shifted_col1, df['#2'])\n    r_squared_values.append(r_squared)\n    shifted_dataframes.append(df.copy())\n    shifted_dataframes[-1]['#1'] = shifted_col1\n\nmin_r_squared = min(r_squared_values)\nmin_r_squared_index = r_squared_values.index(min_r_squared)\ndf = shifted_dataframes[min_r_squared_index]\n"
test_execution(code)

