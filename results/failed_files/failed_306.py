import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array(
                [
                    [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
                    [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
                ]
            )
            shift = 3
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.rand(10, 100)
            shift = np.random.randint(-99, 0)
        return a, shift

    def generate_ans(data):
        _a = data
        a, shift = _a

        def solution(xs, n):
            e = np.empty_like(xs)
            if n >= 0:
                e[:, :n] = np.nan
                e[:, n:] = xs[:, :-n]
            else:
                e[:, n:] = np.nan
                e[:, :n] = xs[:, -n:]
            return e

        result = solution(a, shift)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
a, shift = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\n\ndef shift_1d(arr, shift_amount):\n    new_arr = np.full(arr.shape, np.nan)\n    if shift_amount > 0:\n        new_arr[shift_amount:] = arr[:-shift_amount]\n    elif shift_amount < 0:\n        new_arr[:shift_amount] = arr[-shift_amount:]\n    else:\n        new_arr[:] = arr\n    return new_arr\n\ndef shift(arr, shift_amount):\n    shifted_arr = np.array([shift_1d(row, shift_amount) for row in arr])\n    return shifted_arr\n\nresult = shift(a, shift)\n'
test_execution(code)

