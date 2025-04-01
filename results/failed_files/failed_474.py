import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            c = np.array([[[75, 763]], [[57, 763]], [[np.nan, 749]], [[75, 749]]])
            CNTS = [
                np.array([[[np.nan, 1202]], [[63, 1202]], [[63, 1187]], [[78, 1187]]]),
                np.array([[[75, 763]], [[57, 763]], [[np.nan, 749]], [[75, 749]]]),
                np.array(
                    [
                        [[72, 742]],
                        [[58, 742]],
                        [[57, 741]],
                        [[57, np.nan]],
                        [[58, 726]],
                        [[72, 726]],
                    ]
                ),
                np.array([[[np.nan, 194]], [[51, 194]], [[51, 179]], [[66, 179]]]),
            ]
        elif test_case_id == 2:
            np.random.seed(42)
            c = np.random.rand(3, 4)
            CNTS = [np.random.rand(x, x + 2) for x in range(3, 7)]
        elif test_case_id == 3:
            c = np.array([[[75, 763]], [[57, 763]], [[np.nan, 749]], [[75, 749]]])
            CNTS = [
                np.array([[[np.nan, 1202]], [[63, 1202]], [[63, 1187]], [[78, 1187]]]),
                np.array([[[np.nan, 763]], [[57, 763]], [[20, 749]], [[75, 749]]]),
                np.array(
                    [
                        [[72, 742]],
                        [[58, 742]],
                        [[57, 741]],
                        [[57, np.nan]],
                        [[58, 726]],
                        [[72, 726]],
                    ]
                ),
                np.array([[[np.nan, 194]], [[51, 194]], [[51, 179]], [[66, 179]]]),
            ]
        return c, CNTS

    def generate_ans(data):
        _a = data
        c, CNTS = _a
        temp_c = c.copy()
        temp_c[np.isnan(temp_c)] = 0
        result = False
        for arr in CNTS:
            temp = arr.copy()
            temp[np.isnan(temp)] = 0
            result |= (
                np.array_equal(temp_c, temp) and (np.isnan(c) == np.isnan(arr)).all()
            )
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert result == ans
    return 1


exec_context = r"""
import numpy as np
c, CNTS = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(3):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\n\ndef array_in_list(arr, list_of_arrs):\n    def compare_arrays(arr1, arr2):\n        return np.array_equal(arr1, arr2, equal_nan=True)\n\n    for element in list_of_arrs:\n        if compare_arrays(arr, element):\n            return True\n    return False\n\nc = np.array([[[ 75, 763]],\n              [[ 57, 763]],\n              [[ np.nan, 749]],\n              [[ 75, 749]]])\nCNTS = [np.array([[[  np.nan, 1202]],\n                  [[  63, 1202]],\n                  [[  63, 1187]],\n                  [[  78, 1187]]]),\n        np.array([[[ 75, 763]],\n                  [[ 57, 763]],\n                  [[ np.nan, 749]],\n                  [[ 75, 749]]]),\n        np.array([[[ 72, 742]],\n                  [[ 58, 742]],\n                  [[ 57, 741]],\n                  [[ 57, np.nan]],\n                  [[ 58, 726]],\n                  [[ 72, 726]]]),\n        np.array([[[ np.nan, 194]],\n                  [[ 51, 194]],\n                  [[ 51, 179]],\n                  [[ 66, 179]]])]\n\nresult = array_in_list(c, CNTS)\n'
test_execution(code)

