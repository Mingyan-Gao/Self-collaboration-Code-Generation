import numpy as np
import copy
import scipy
from scipy.integrate import simpson


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            x = np.linspace(0, 1, 20)
            y = np.linspace(0, 1, 30)
        elif test_case_id == 2:
            x = np.linspace(3, 5, 30)
            y = np.linspace(0, 1, 20)
        return x, y

    def generate_ans(data):
        _a = data
        x, y = _a
        z = np.cos(x[:, None]) ** 4 + np.sin(y) ** 2
        result = simpson(simpson(z, y), x)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))

    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
x, y = test_input
def f(x, y):
[insert]
result = f(x, y)
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\n    X, Y = np.meshgrid(x, y)\n    func_values = (np.cos(X)**4) + (np.sin(Y)**2)\n    \n    def simpson_weights(n):\n        weights = np.ones(n)\n        weights[1:-1:2] = 4\n        weights[2:-1:2] = 2\n        return weights\n    \n    x_weights = simpson_weights(len(x))\n    y_weights = simpson_weights(len(y))\n    \n    weights_2d = np.outer(y_weights, x_weights)\n    \n    weighted_values = func_values * weights_2d\n    \n    integral_value = np.sum(weighted_values)\n    \n    dx = x[1] - x[0]\n    dy = y[1] - y[0]\n    \n    integral_value *= dx * dy / 9\n    \n    return integral_value\n### END SOLUTION\n'
test_execution(code)

