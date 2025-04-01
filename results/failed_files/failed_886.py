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

code = '\nfrom scipy import stats\nfrom sklearn.preprocessing import StandardScaler\n\ndef load_data():\n    np.random.seed(1)\n    x1 = np.random.normal(loc=5, scale=2, size=1000)\n    x2 = np.random.exponential(scale=1/10, size=1000)\n    return np.column_stack((x1, x2))\n\ndata = load_data()\n\nx1_transformed, _ = stats.boxcox(data[:, 0] - np.min(data[:, 0]) + 1)\nx2_transformed, _ = stats.boxcox(data[:, 1] - np.min(data[:, 1]) + 1)\n\ntransformed_data = np.column_stack((x1_transformed, x2_transformed))\n\nscaler = StandardScaler()\ncentered_scaled_data = scaler.fit_transform(transformed_data)\n'
test_execution(code)
test_string(code)
