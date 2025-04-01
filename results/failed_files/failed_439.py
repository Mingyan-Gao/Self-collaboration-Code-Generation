import numpy as np
import pandas as pd
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            np.random.seed(42)
            X = np.random.randint(2, 10, (5, 6))
        elif test_case_id == 2:
            np.random.seed(42)
            X = np.random.rand(10, 20)
        return X

    def generate_ans(data):
        _a = data
        X = _a
        result = X.T[:, :, None] * X.T[:, None]
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
X = test_input
[insert]
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

code = '\nimport numpy as np\nX = np.random.randint(2, 10, (5, 6))\nN = X.shape[1]\nM = X.shape[0]\nresult = np.zeros((N, M, M))\nfor i in range(N):\n    xi = X[:, i]\n    result[i, :, :] = np.outer(xi, xi)\n'
test_execution(code)
test_string(code)
