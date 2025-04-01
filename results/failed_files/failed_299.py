import numpy as np
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array([[1, 0, 3], [2, 4, 1]])
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.randint(0, 20, (10, 20))
        return a

    def generate_ans(data):
        _a = data
        a = _a
        temp = (a - a.min()).ravel()
        b = np.zeros((a.size, temp.max() + 1))
        b[np.arange(a.size), temp] = 1
        return b

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
result = b
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)


def test_string(solution: str):
    tokens = []
    for token in tokenize.tokenize(io.BytesIO(solution.encode("utf-8")).readline):
        tokens.append(token.string)
    assert "while" not in tokens and "for" not in tokens

code = '\n    min_val = np.min(a)\n    max_val = np.max(a)\n    rows, cols = a.shape\n    b = np.zeros((rows * cols, max_val - min_val + 1), dtype=int)\n    a_flat = a.flatten()\n    indices = a_flat - min_val\n    row_indices = np.arange(rows * cols)\n    b[row_indices, indices] = 1\n'
test_execution(code)
test_string(code)
