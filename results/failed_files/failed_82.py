import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        df["A"].replace(to_replace=0, method="ffill", inplace=True)
        return df

    def define_test_input(test_case_id):
        if test_case_id == 1:
            index = range(14)
            data = [1, 0, 0, 2, 0, 4, 6, 8, 0, 0, 0, 0, 2, 1]
            df = pd.DataFrame(data=data, index=index, columns=["A"])
        if test_case_id == 2:
            index = range(14)
            data = [1, 0, 0, 9, 0, 2, 6, 8, 0, 0, 0, 0, 1, 7]
            df = pd.DataFrame(data=data, index=index, columns=["A"])
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

code = "\ndf['A'] = df['A'].replace(0, pd.NA).fillna(method='ffill')\n"
test_execution(code)

