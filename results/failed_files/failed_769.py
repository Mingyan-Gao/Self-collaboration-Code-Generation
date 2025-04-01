import numpy as np
import copy
import tokenize, io
from scipy.sparse import csr_matrix


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            arr = np.array(
                [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
            )
            row = 2
            column = 3
        elif test_case_id == 2:
            np.random.seed(42)
            arr = np.random.randint(0, 3, (10, 10))
            row = np.random.randint(0, 8)
            column = np.random.randint(0, 8)
        M = csr_matrix(arr)
        return M, row, column

    def generate_ans(data):
        _a = data
        M, row, column = _a
        result = M[row, column]
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
from scipy.sparse import csr_matrix
M, row, column = test_input
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
    assert (
        "toarray" not in tokens
        and "array" not in tokens
        and "todense" not in tokens
        and "A" not in tokens
    )

code = '\nimport numpy as np\nfrom scipy.sparse import csr_matrix\n\narr = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])\nM = csr_matrix(arr)\nrow = 2\ncolumn = 3\n\nresult = M.getrow(row).toarray()[0, column]\n'
test_execution(code)
test_string(code)
