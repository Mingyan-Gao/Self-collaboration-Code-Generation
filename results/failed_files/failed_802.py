import numpy as np
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array([[26, 3, 0], [3, 195, 1], [0, 1, 17]])
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.randint(0, 10, (5, 6))
        return a

    def generate_ans(data):
        _a = data
        a = _a
        a = 1 - np.sign(a)
        return a

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import scipy
import numpy as np
a = test_input
[insert]
result = a
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nn = a.shape[0]\nb = np.zeros((n, n))\nfor i in range(n):\n    for j in range(i, n):\n        if a[i, j] == 0:\n            b[i, j] = 1\n        else:\n            b[i, j] = 0\n        b[j, i] = b[i, j]\na = b\n'
test_execution(code)

