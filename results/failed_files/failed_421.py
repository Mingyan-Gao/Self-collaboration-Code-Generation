import numpy as np
import copy
import scipy
from scipy.special import comb


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            x = 0.25
            x_min = 0
            x_max = 1
            N = 5
        elif test_case_id == 2:
            x = 0.25
            x_min = 0
            x_max = 1
            N = 8
        elif test_case_id == 3:
            x = -1
            x_min = 0
            x_max = 1
            N = 5
        elif test_case_id == 4:
            x = 2
            x_min = 0
            x_max = 1
            N = 7
        return x, x_min, x_max, N

    def generate_ans(data):
        _a = data
        x, x_min, x_max, N = _a

        def smoothclamp(x, x_min=0, x_max=1, N=1):
            if x < x_min:
                return x_min
            if x > x_max:
                return x_max
            x = np.clip((x - x_min) / (x_max - x_min), 0, 1)
            result = 0
            for n in range(0, N + 1):
                result += comb(N + n, n) * comb(2 * N + 1, N - n) * (-x) ** n
            result *= x ** (N + 1)
            return result

        result = smoothclamp(x, N=N)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))

    return test_input, expected_result


def exec_test(result, ans):
    assert abs(ans - result) <= 1e-5
    return 1


exec_context = r"""
import numpy as np
x, x_min, x_max, N = test_input
[insert]
result = smoothclamp(x, N=N)
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(4):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\ndef smoothstep(t, N):\n    t = np.clip(t, 0.0, 1.0)\n    result = t**N * (np.poly1d([np.math.factorial(N + 1) / (np.math.factorial(N + 1 - k) * np.math.factorial(k)) * (-1)**k for k in range(N + 1)][::-1]))(t)\n    return result\n\ndef smoothclamp(x, min_val, max_val, N):\n    if min_val > max_val:\n        min_val, max_val = max_val, min_val\n\n    if max_val == min_val:\n        return float(min_val)\n\n    t = (x - min_val) / (max_val - min_val)\n    t = smoothstep(t, N)\n    \n    return float(min_val + t * (max_val - min_val))\n'
test_execution(code)

