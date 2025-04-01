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
                    "bit1": [0, 2, 4],
                    "bit2": [0, 2, 0],
                    "bit3": [3, 0, 4],
                    "bit4": [3, 0, 4],
                    "bit5": [0, 2, 4],
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

code = "\nimport pandas as pd\n\ndf = pd.DataFrame({'bit1': [0, 2, 4],\n                   'bit2': [0, 2, 0],\n                   'bit3': [3, 0, 4],\n                   'bit4': [3, 0, 4],\n                   'bit5': [0, 2, 4]})\n\nfrequent_values = []\nfrequency_counts = []\n\nfor index, row in df.iterrows():\n    value_counts = row.value_counts()\n    most_frequent_value = value_counts.idxmax()\n    max_count = value_counts.max()\n    frequent_values.append(most_frequent_value)\n    frequency_counts.append(max_count)\n\ndf['frequent'] = frequent_values\ndf['freq_count'] = frequency_counts\n"
test_execution(code)

