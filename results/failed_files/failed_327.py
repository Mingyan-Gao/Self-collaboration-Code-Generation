import numpy as np
import pandas as pd
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
            length = np.random.randint(12, 18)
        return A, length

    def generate_ans(data):
        _a = data
        A, length = _a
        result = np.pad(A, (0, length - A.shape[0]), "constant")
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

code = '\nimport numpy as np\nimport math\n\ndef pad(A, length):\n    if len(A) >= length:\n        return A\n    else:\n        pad_size = length - len(A)\n        return np.concatenate([A, np.zeros(pad_size)])\n\ndef nearest_multiple_1024(x):\n    return int(math.ceil(x / 1024) * 1024)\n\ndef pad_to_nearest_1024(A):\n    length = nearest_multiple_1024(len(A))\n    return pad(A, length)\n\nA = np.array([1,2,3,4,5])\nlength = 8\nresult = pad(A, length)\n'
test_execution(code)
test_string(code)
