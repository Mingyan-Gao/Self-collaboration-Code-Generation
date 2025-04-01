import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array([1, 2, 3, 4, 5])
            m = 8
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.randint(0, 100, (20,))
            m = np.random.randint(10, 15)
        return a, m

    def generate_ans(data):
        _a = data
        a, m = _a
        result = (((a[:, None] & (1 << np.arange(m))[::-1])) > 0).astype(int)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
a, m = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\na = np.array([1, 2, 3, 4, 5])\nm = 8\n\ndef int_to_binary_array(num, m):\n    binary_array = np.zeros(m, dtype=int)\n    for i in range(m - 1, -1, -1):\n        binary_array[m - 1 - i] = (num >> i) & 1\n    return binary_array\n\nresult = np.stack([int_to_binary_array(num, m) for num in a])\n'
test_execution(code)

