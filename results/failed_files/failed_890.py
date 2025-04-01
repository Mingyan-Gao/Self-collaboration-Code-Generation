import numpy as np
import copy
import tokenize, io
import sklearn
from sklearn.preprocessing import PowerTransformer


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            data = np.array([[1, 2], [3, 2], [4, 5]])
        return data

    def generate_ans(data):
        def ans1(data):
            pt = PowerTransformer(method="yeo-johnson")
            yeo_johnson_data = pt.fit_transform(data)
            return yeo_johnson_data

        def ans2(data):
            pt = PowerTransformer(method="yeo-johnson", standardize=False)
            yeo_johnson_data = pt.fit_transform(data)
            return yeo_johnson_data

        return ans1(copy.deepcopy(data)), ans2(copy.deepcopy(data))

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))

    return test_input, expected_result


def exec_test(result, ans):
    ret = 0
    try:
        np.testing.assert_allclose(result, ans[0])
        ret = 1
    except:
        pass
    try:
        np.testing.assert_allclose(result, ans[1])
        ret = 1
    except:
        pass
    return ret


exec_context = r"""
import pandas as pd
import numpy as np
import sklearn
data = test_input
[insert]
result = yeo_johnson_data
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)


def test_string(solution: str):
    tokens = []
    for token in tokenize.tokenize(io.BytesIO(solution.encode("utf-8")).readline):
        tokens.append(token.string)
    assert "sklearn" in tokens

code = "\nfrom sklearn.preprocessing import PowerTransformer, StandardScaler\ndef load_data():\n    np.random.seed(1)\n    x1 = np.random.normal(loc=5, scale=2, size=1000)\n    x2 = np.random.exponential(scale=1/10, size=1000)\n    predictors = np.column_stack((x1, x2))\n    return predictors\ndata = load_data()\nassert type(data) == np.ndarray\npt = PowerTransformer(method='yeo-johnson', standardize=False)\nyeo_johnson_data = pt.fit_transform(data)\nscaler = StandardScaler()\nyeo_johnson_data = scaler.fit_transform(yeo_johnson_data)\n"
test_execution(code)
test_string(code)
