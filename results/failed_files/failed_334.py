import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array([10, 20, 30])
            b = np.array([30, 20, 20])
            c = np.array([50, 20, 40])
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.rand(50)
            b = np.random.rand(50)
            c = np.random.rand(50)
        return a, b, c

    def generate_ans(data):
        _a = data
        a, b, c = _a
        result = np.mean([a, b, c], axis=0)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
a, b, c = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\n\ndef elementwise_average(*arrays):\n    if not all(isinstance(arr, np.ndarray) for arr in arrays):\n        raise ValueError("All inputs must be NumPy arrays.")\n    \n    if len(set(arr.shape for arr in arrays)) > 1:\n        raise ValueError("All input arrays must have the same shape.")\n    \n    sum_array = np.sum(arrays, axis=0)\n    average_array = sum_array / len(arrays)\n    return average_array\n\na = np.array([10, 20, 30])\nb = np.array([30, 20, 20])\nc = np.array([50, 20, 40])\n\nresult = elementwise_average(a, b, c)\n'
test_execution(code)

