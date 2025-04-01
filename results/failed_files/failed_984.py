import numpy as np
import torch
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            torch.random.manual_seed(42)
            A = torch.randint(2, (100,))
            torch.random.manual_seed(7)
            B = torch.randint(2, (100,))
        return A, B

    def generate_ans(data):
        A, B = data
        cnt_equal = int((A[int(len(A) / 2) :] == B[int(len(A) / 2) :]).sum())
        return cnt_equal

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        np.testing.assert_equal(int(result), ans)
        return 1
    except:
        return 0


exec_context = r"""
import numpy as np
import pandas as pd
import torch
A, B = test_input
[insert]
result = cnt_equal
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)


def test_string(solution: str):
    tokens = []
    for token in tokenize.tokenize(io.BytesIO(solution.encode("utf-8")).readline):
        tokens.append(token.string)
    assert "for" not in tokens and "while" not in tokens

code = '\n    x = A.shape[0] // 2\n    cnt_equal = torch.sum((A[-x:] == B[-x:]).int())\n'
test_execution(code)
test_string(code)
