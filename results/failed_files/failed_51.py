import pandas as pd
import numpy as np
import math
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return df.join(df.apply(lambda x: math.e**x).add_prefix("exp_"))

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        if test_case_id == 2:
            df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
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


def test_string(solution: str):
    tokens = []
    for token in tokenize.tokenize(io.BytesIO(solution.encode("utf-8")).readline):
        tokens.append(token.string)
    assert "while" not in tokens and "for" not in tokens

code = "\nimport numpy as np\n\nfor col in df.columns:\n    df[f'exp_{col} '] = np.exp(df[col])\nresult = df\n"
test_execution(code)
test_string(code)
