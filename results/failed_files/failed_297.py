import numpy as np
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array([-1, 0, 3])
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.randint(-5, 20, 50)
        return a

    def generate_ans(data):
        _a = data
        a = _a
        temp = a - a.min()
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

code = '\n    min_a = np.min(a)\n    range_a = np.max(a) - min_a + 1\n    b = np.zeros((len(a), range_a), dtype=int)\n    row_indices = np.arange(len(a))\n    col_indices = a - min_a\n    b[row_indices, col_indices] = 1\n'
test_execution(code)
test_string(code)
