import numpy as np
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array([[0, 1], [2, 1], [4, 8]])
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.rand(10, 5)
        return a

    def generate_ans(data):
        _a = data
        a = _a
        mask = a.min(axis=1, keepdims=1) == a
        return mask

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
result = mask
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\na = np.array([[0, 1], [2, 1], [4, 8]])\nmin_ind = np.argmin(a, axis=1)\nmask = np.zeros(a.shape, dtype=bool)\nrow_ind = np.arange(a.shape[0])\nmask[row_ind, min_ind] = True\n'
test_execution(code)

