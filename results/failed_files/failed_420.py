import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            x = 0.25
            x_min = 0
            x_max = 1
        elif test_case_id == 2:
            x = -1
            x_min = 0
            x_max = 1
        elif test_case_id == 3:
            x = 2
            x_min = 0
            x_max = 1
        return x, x_min, x_max

    def generate_ans(data):
        _a = data
        x, x_min, x_max = _a

        def smoothclamp(x):
            return np.where(
                x < x_min, x_min, np.where(x > x_max, x_max, 3 * x**2 - 2 * x**3)
            )

        result = smoothclamp(x)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert abs(ans - result) <= 1e-5
    return 1


exec_context = r"""
import numpy as np
x, x_min, x_max = test_input
[insert]
result = smoothclamp(x)
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(3):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\ndef smoothclamp(x, min, max):\n    if min > max:\n        return min\n    if x < min:\n        return min\n    if x > max:\n        return max\n    margin = (max - min) * 0.1\n    if min <= x <= min + margin:\n        def smoothstep(x):\n            return 3 * x**2 - 2 * x**3\n        normalized_x = (x - min) / margin\n        return min + smoothstep(normalized_x) * margin\n    if max - margin <= x <= max:\n        def smoothstep(x):\n            return 3 * x**2 - 2 * x**3\n        normalized_x = (x - (max - margin)) / margin\n        return max - smoothstep(normalized_x) * margin\n    return x\n'
test_execution(code)

