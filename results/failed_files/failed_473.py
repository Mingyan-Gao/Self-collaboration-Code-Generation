import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            c = np.array([[[75, 763]], [[57, 763]], [[57, 749]], [[75, 749]]])
            CNTS = [
                np.array([[[78, 1202]], [[63, 1202]], [[63, 1187]], [[78, 1187]]]),
                np.array([[[75, 763]], [[57, 763]], [[57, 749]], [[75, 749]]]),
                np.array(
                    [
                        [[72, 742]],
                        [[58, 742]],
                        [[57, 741]],
                        [[57, 727]],
                        [[58, 726]],
                        [[72, 726]],
                    ]
                ),
                np.array([[[66, 194]], [[51, 194]], [[51, 179]], [[66, 179]]]),
            ]
        elif test_case_id == 2:
            np.random.seed(42)
            c = np.random.rand(3, 4)
            CNTS = [np.random.rand(x, x + 2) for x in range(3, 7)]
        elif test_case_id == 3:
            c = np.array([[[75, 763]], [[57, 763]], [[57, 749]], [[75, 749]]])
            CNTS = [
                np.array([[[75, 763]], [[57, 763]], [[57, 749]], [[75, 749]]]),
                np.array(
                    [
                        [[72, 742]],
                        [[58, 742]],
                        [[57, 741]],
                        [[57, 727]],
                        [[58, 726]],
                        [[72, 726]],
                    ]
                ),
                np.array([[[66, 194]], [[51, 194]], [[51, 179]], [[66, 179]]]),
            ]
        return c, CNTS

    def generate_ans(data):
        _a = data
        c, CNTS = _a
        result = any(np.array_equal(c, x) for x in CNTS)
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

code = '\nimport numpy as np\n\ndef are_equal(arr1, arr2):\n    return np.array_equal(arr1, arr2)\n\ndef is_member(arr, arr_list):\n    for element in arr_list:\n        if are_equal(arr, element):\n            return True\n    return False\n\ndef remove_array(arr, arr_list):\n    for i, element in enumerate(arr_list):\n        if are_equal(arr, element):\n            del arr_list[i]\n            return arr_list\n    return arr_list\n\nc = np.array([[[ 75, 763]],\n              [[ 57, 763]],\n              [[ 57, 749]],\n              [[ 75, 749]]])\nCNTS = [np.array([[[  78, 1202]],\n                  [[  63, 1202]],\n                  [[  63, 1187]],\n                  [[  78, 1187]]]),\n        np.array([[[ 75, 763]],\n                  [[ 57, 763]],\n                  [[ 57, 749]],\n                  [[ 75, 749]]]),\n        np.array([[[ 72, 742]],\n                  [[ 58, 742]],\n                  [[ 57, 741]],\n                  [[ 57, 727]],\n                  [[ 58, 726]],\n                  [[ 72, 726]]]),\n        np.array([[[ 66, 194]],\n                  [[ 51, 194]],\n                  [[ 51, 179]],\n                  [[ 66, 179]]])]\n\nresult = is_member(c, CNTS)\n'
test_execution(code)

