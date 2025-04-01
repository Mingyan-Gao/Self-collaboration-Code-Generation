import numpy as np
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array(
                [
                    [[0, 1, 2, 3], [2, 3, 4, 5], [4, 5, 6, 7]],
                    [[6, 7, 8, 9], [8, 9, 10, 11], [10, 11, 12, 13]],
                    [[12, 13, 14, 15], [14, 15, 16, 17], [16, 17, 18, 19]],
                ]
            )
            b = np.array([[0, 1, 2], [2, 1, 3], [1, 0, 3]])
        elif test_case_id == 2:
            np.random.seed(42)
            dim = np.random.randint(10, 15)
            T = np.random.randint(5, 8)
            a = np.random.rand(dim, dim, T)
            b = np.zeros((dim, dim)).astype(int)
            for i in range(T):
                row = np.random.randint(0, dim - 1, (5,))
                col = np.random.randint(0, dim - 1, (5,))
                b[row, col] = i
        return a, b

    def generate_ans(data):
        _a = data
        a, b = _a
        arr = np.take_along_axis(a, b[..., np.newaxis], axis=-1)[..., 0]
        result = np.sum(a) - np.sum(arr)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
a, b = test_input
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

code = '\nimport numpy as np\na = np.array( \n    [[[ 0,  1, 2, 3],\n     [ 2,  3, 4, 5],\n     [ 4,  5, 6, 7]],\n    [[ 6,  7, 8, 9],\n     [ 8,  9, 10, 11],\n     [10, 11, 12, 13]],\n    [[12, 13, 14, 15],\n     [14, 15, 16, 17],\n     [16, 17, 18, 19]]]\n)\nb = np.array( \n    [[0, 1, 2],\n    [2, 1, 3],\n[1, 0, 3]]\n)\nresult = 0\nfor i in np.ndindex(b.shape):\n    result += np.sum(a[i[0], i[1], np.arange(a.shape[2]) != b[i]])\n'
test_execution(code)
test_string(code)
