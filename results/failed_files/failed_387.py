import numpy as np
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array(
                [[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]]
            )
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.rand(100, 200)
        return a

    def generate_ans(data):
        _a = data
        a = _a
        result = (
            a.reshape(a.shape[0] // 2, 2, a.shape[1] // 2, 2)
            .swapaxes(1, 2)
            .reshape(-1, 2, 2)
        )
        return result

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

code = '\nresult = a.reshape(2, 2, 2, 2).transpose(0, 2, 1, 3).reshape(-1, 2, 2)\n'
test_execution(code)
test_string(code)
