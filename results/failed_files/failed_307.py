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
            shift = [-2, 3]
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.rand(10, 100)
            shift = np.random.randint(-99, 99, (10,))
        return a, shift

    def generate_ans(data):
        _a = data
        a, shift = _a

        def solution(xs, shift):
            e = np.empty_like(xs)
            for i, n in enumerate(shift):
                if n >= 0:
                    e[i, :n] = np.nan
                    e[i, n:] = xs[i, :-n]
                else:
                    e[i, n:] = np.nan
                    e[i, :n] = xs[i, -n:]
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

code = '\nimport numpy as np\n\ndef shift_array(arr, shift_value):\n    new_arr = np.full(arr.shape, np.nan)\n    if shift_value > 0:\n        new_arr[shift_value:] = arr[:-shift_value]\n    elif shift_value < 0:\n        new_arr[:shift_value] = arr[-shift_value:]\n    else:\n        new_arr[:] = arr\n    return new_arr\n\ndef shift(array_2d, shift_list):\n    if len(shift_list) != array_2d.shape[0]:\n        raise ValueError("The length of shift_list must be equal to the number of rows in array_2d.")\n    \n    shifted_rows = []\n    for i, row in enumerate(array_2d):\n        shifted_row = shift_array(row, shift_list[i])\n        shifted_rows.append(shifted_row)\n    \n    return np.array(shifted_rows)\n\nresult = shift(a, shift)\n'
test_execution(code)

