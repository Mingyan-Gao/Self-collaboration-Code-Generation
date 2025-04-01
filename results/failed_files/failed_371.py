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
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\n\ndef simpson_2d_weights(x_size, y_size):\n    weights = np.ones((y_size, x_size))\n    weights[1:-1, 1:-1] = 4\n    weights[1:-1, 0] = 2\n    weights[1:-1, -1] = 2\n    weights[0, 1:-1] = 2\n    weights[-1, 1:-1] = 2\n    weights[0, 0] = 1\n    weights[0, -1] = 1\n    weights[-1, 0] = 1\n    weights[-1, -1] = 1\n    return weights\n\ndef evaluate_function(x, y):\n    X, Y = np.meshgrid(x, y)\n    return np.cos(X)**4 + np.sin(Y)**2\n\ndef integrate_2d(function_values, weights, dx, dy):\n    return dx * dy / 9 * np.sum(function_values * weights)\n\nx = np.linspace(0, 1, 20)\ny = np.linspace(0, 1, 30)\n\nweights = simpson_2d_weights(len(x), len(y))\nfunction_values = evaluate_function(x, y)\ndx = x[1] - x[0]\ndy = y[1] - y[0]\nresult = integrate_2d(function_values, weights, dx, dy)\n'
test_execution(code)

