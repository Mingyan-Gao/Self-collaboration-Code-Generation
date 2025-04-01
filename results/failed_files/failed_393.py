import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array(
                [
                    [0, 1, 2, 3, 5, 6, 7, 8],
                    [4, 5, 6, 7, 5, 3, 2, 5],
                    [8, 9, 10, 11, 4, 5, 3, 5],
                ]
            )
            low = 1
            high = 10
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.rand(20, 10)
            low = np.random.randint(1, 8)
            high = np.random.randint(low + 1, 10)
        return a, low, high

    def generate_ans(data):
        _a = data
        a, low, high = _a
        high = min(high, a.shape[1])
        result = a[:, low:high]
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
a, low, high = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\na = np.array([[ 0,  1,  2,  3, 5, 6, 7, 8],\n              [ 4,  5,  6,  7, 5, 3, 2, 5],\n              [ 8,  9, 10, 11, 4, 5, 3, 5]])\nlow = 1\nhigh = 10\nmax_col = a.shape[1] - 1\nhigh = min(high, max_col)\nresult = a[:, low:high+1]\n'
test_execution(code)

