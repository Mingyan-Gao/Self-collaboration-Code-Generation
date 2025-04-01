import numpy as np
import copy
import tokenize, io
import scipy
from scipy.stats import ks_2samp


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            low = 1
            high = np.e
            size = 10000
        return low, high, size

    def generate_ans(data):
        _a = data
        min, max, n = _a
        result = scipy.stats.loguniform.rvs(a=min, b=max, size=n)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))

    return test_input, expected_result


def exec_test(result, ans):

    np.testing.assert_array_equal(result.shape, ans.shape)
    assert ks_2samp(result, ans)[0] <= 0.1

    return 1


exec_context = r"""
import numpy as np
min, max, n = test_input
def f(min=1, max=np.e, n=10000):
[insert]
result = f(min, max, n)
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
    assert "while" not in tokens and "for" not in tokens

code = '\nimport numpy as np\ndef f(min=1, max=np.e, n=10000):\n    # return the solution in this function\n    # result = f(min=1, max=np.e, n=10000)\n    ### BEGIN SOLUTION\n    def loguniform(n, min, max, base=np.e):\n        if min <= 0 or max <= 0:\n            raise ValueError("min and max must be positive numbers")\n        if min >= max:\n            raise ValueError("min must be less than max")\n        if not isinstance(n, int) or n <= 0:\n            raise ValueError("n must be a positive integer")\n\n        log_min = np.log(min) / np.log(base)\n        log_max = np.log(max) / np.log(base)\n        uniform_values = np.random.uniform(log_min, log_max, n)\n        return base ** uniform_values\n    return loguniform(n, min, max)\n    ### END SOLUTION\n'
test_execution(code)
test_string(code)
