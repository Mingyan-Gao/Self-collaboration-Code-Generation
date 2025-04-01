import numpy as np
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            A = np.array([1, 2, 3, 4, 5])
            length = 8
        elif test_case_id == 2:
            np.random.seed(42)
            A = np.random.rand(10)
            length = np.random.randint(6, 14)
        elif test_case_id == 3:
            A = np.array([1, 2, 3, 4, 5])
            length = 3
        return A, length

    def generate_ans(data):
        _a = data
        A, length = _a
        if length > A.shape[0]:
            result = np.pad(A, (0, length - A.shape[0]), "constant")
        else:
            result = A.copy()
            result[length:] = 0
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
A, length = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(3):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)


def test_string(solution: str):
    tokens = []
    for token in tokenize.tokenize(io.BytesIO(solution.encode("utf-8")).readline):
        tokens.append(token.string)
    assert "while" not in tokens and "for" not in tokens

code = '\nimport numpy as np\n\ndef pad(A, length):\n    if length <= len(A):\n        return np.concatenate((A[:length], np.zeros(len(A) - length, dtype=A.dtype))) if len(A) > length else A[:length]\n    else:\n        new_array = np.zeros(length, dtype=A.dtype)\n        new_array[:len(A)] = A\n        return new_array\n\ndef pad_to_multiple(A):\n    target_length = (len(A) + 1023) // 1024 * 1024\n    return pad(A, target_length)\n\nA = np.array([1,2,3,4,5])\nlength = 8\nresult = pad(A, length)\n'
test_execution(code)
test_string(code)
