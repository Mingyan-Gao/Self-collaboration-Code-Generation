import numpy as np
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array([0, 0, 1, 1, 1, 2, 2, 0, 1, 3, 3, 3])
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.randint(0, 3, (20,))
        return a

    def generate_ans(data):
        _a = data
        a = _a
        selection = np.ones(len(a), dtype=bool)
        selection[1:] = a[1:] != a[:-1]
        selection &= a != 0
        result = a[selection]
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
a = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nfiltered_arr = a[a != 0]\nresult_list = []\nif len(filtered_arr) > 0:\n    result_list.append(filtered_arr[0])\n    for i in range(1, len(filtered_arr)):\n        if filtered_arr[i] != filtered_arr[i-1]:\n            result_list.append(filtered_arr[i])\nresult = np.array(result_list)\n'
test_execution(code)

