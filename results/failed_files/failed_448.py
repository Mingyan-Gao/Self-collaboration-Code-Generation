import numpy as np
import pandas as pd
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            x_dists = np.array([[0, -1, -2], [1, 0, -1], [2, 1, 0]])
            y_dists = np.array([[0, 1, -2], [-1, 0, 1], [-2, 1, 0]])
        elif test_case_id == 2:
            np.random.seed(42)
            x_dists = np.random.rand(3, 4)
            y_dists = np.random.rand(3, 4)
        return x_dists, y_dists

    def generate_ans(data):
        _a = data
        x_dists, y_dists = _a
        dists = np.vstack(([x_dists.T], [y_dists.T])).T
        return dists

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
x_dists, y_dists = test_input
[insert]
result = dists
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

code = '\nimport numpy as np\nx_dists = np.array([[ 0, -1, -2],\n                 [ 1,  0, -1],\n                 [ 2,  1,  0]])\n\ny_dists = np.array([[ 0, 1, -2],\n                 [ -1,  0, 1],\n                 [ -2,  1,  0]])\ndists = np.stack((x_dists, y_dists), axis=-1)\n'
test_execution(code)
test_string(code)
