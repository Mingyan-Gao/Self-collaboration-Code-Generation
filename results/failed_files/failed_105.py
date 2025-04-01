import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        df.loc[df["name"].str.split().str.len() == 2, "last_name"] = (
            df["name"].str.split().str[-1]
        )
        df.loc[df["name"].str.split().str.len() == 2, "name"] = (
            df["name"].str.split().str[0]
        )
        df.rename(columns={"name": "first_name"}, inplace=True)
        return df

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {"name": ["Jack Fine", "Kim Q. Danger", "Jane Smith", "Zhongli"]}
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
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\ndef split_name(name):\n    parts = name.split()\n    if len(parts) == 2:\n        first_name = parts[0]\n        last_name = parts[1]\n    else:\n        first_name = name\n        last_name = None\n    return first_name, last_name\n\ndf[['first_name', 'last_name']] = df['name'].apply(lambda x: pd.Series(split_name(x)))\n"
test_execution(code)

