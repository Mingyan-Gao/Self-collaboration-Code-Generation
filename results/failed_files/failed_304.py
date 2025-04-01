import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            A = np.array([1, 2, 3, 4, 5, 6, 7])
            ncol = 2
        elif test_case_id == 2:
            np.random.seed(42)
            A = np.random.rand(23)
            ncol = 5
        return A, ncol

    def generate_ans(data):
        _a = data
        A, ncol = _a
        col = (A.shape[0] // ncol) * ncol
        B = A[len(A) - col :][::-1]
        B = np.reshape(B, (-1, ncol))
        return B

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
A, ncol = test_input
[insert]
result = B
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nA = np.array([1,2,3,4,5,6,7])\nncol = 2\ndiscard = len(A) % ncol\nA_sliced = A[discard:]\nA_reversed = A_sliced[::-1]\nB = A_reversed.reshape(-1, ncol)\n'
test_execution(code)

