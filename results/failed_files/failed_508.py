import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            A = np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                ]
            )
        elif test_case_id == 2:
            np.random.seed(42)
            A = np.random.randint(0, 2, (10, 10))
        return A

    def generate_ans(data):
        _a = data
        A = _a
        B = np.argwhere(A)
        (ystart, xstart), (ystop, xstop) = B.min(0), B.max(0) + 1
        result = A[ystart:ystop, xstart:xstop]
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
A = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\n\ndef truncate_array(arr):\n    row_indices = np.where(np.any(arr, axis=1))[0]\n    col_indices = np.where(np.any(arr, axis=0))[0]\n    \n    if len(row_indices) == 0 or len(col_indices) == 0:\n        return np.array([])\n\n    row_start, row_end = row_indices[0], row_indices[-1]\n    col_start, col_end = col_indices[0], col_indices[-1]\n    \n    truncated_arr = arr[row_start:row_end+1, col_start:col_end+1]\n    return truncated_arr\n\nA = np.array([[0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 1, 0, 0, 0, 0],\n           [0, 0, 1, 1, 0, 0, 0],\n           [0, 0, 0, 0, 1, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0]])\n\nresult = truncate_array(A)\n'
test_execution(code)

