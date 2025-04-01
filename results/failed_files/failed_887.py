import numpy as np
import copy
import tokenize, io
import sklearn
from sklearn import preprocessing


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            data = np.array([[1, 2], [3, 2], [4, 5]])
        elif test_case_id == 2:
            data = np.array([1, 2, 3, 2, 4, 5])
        return data

    def generate_ans(data):
        data = data
        centered_scaled_data = preprocessing.scale(data)
        return centered_scaled_data

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))

    return test_input, expected_result


def exec_test(result, ans):
    try:
        np.testing.assert_allclose(result, ans)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
import sklearn
data = test_input
[insert]
result = centered_scaled_data
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
    assert "sklearn" in tokens

code = '\nfrom sklearn.preprocessing import PowerTransformer\n\npt = PowerTransformer()\ncentered_scaled_data = pt.fit_transform(data)\n'
test_execution(code)
test_string(code)
