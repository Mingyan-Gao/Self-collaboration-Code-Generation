import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            X = np.array(
                [
                    [[81, 63, 63], [63, 49, 49], [63, 49, 49]],
                    [[4, 12, 8], [12, 36, 24], [8, 24, 16]],
                    [[25, 35, 25], [35, 49, 35], [25, 35, 25]],
                    [[25, 30, 10], [30, 36, 12], [10, 12, 4]],
                ]
            )
        elif test_case_id == 2:
            np.random.seed(42)
            X = np.random.rand(10, 5, 5)
        return X

    def generate_ans(data):
        _a = data
        Y = _a
        X = np.zeros([Y.shape[1], Y.shape[0]])
        for i, mat in enumerate(Y):
            diag = np.sqrt(np.diag(mat))
            X[:, i] += diag
        return X

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
Y = test_input
[insert]
result = X
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\n\nN, M, _ = Y.shape\nX = np.zeros((M, N))\nfor i in range(N):\n    eigenvalues, eigenvectors = np.linalg.eig(Y[i])\n    largest_eigenvalue_index = np.argmax(eigenvalues)\n    largest_eigenvector = eigenvectors[:, largest_eigenvalue_index]\n    x_i = largest_eigenvector * np.sqrt(eigenvalues[largest_eigenvalue_index])\n    X[:, i] = x_i\n'
test_execution(code)

