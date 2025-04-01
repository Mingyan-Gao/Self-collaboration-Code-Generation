import torch
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            torch.random.manual_seed(42)
            a = torch.randn(2, 11)
            b = torch.randn(1, 11)
        elif test_case_id == 2:
            torch.random.manual_seed(7)
            a = torch.randn(2, 11)
            b = torch.randn(1, 11)
        return a, b

    def generate_ans(data):
        a, b = data
        ab = torch.cat((a, b), 0)
        return ab

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        torch.testing.assert_close(result, ans, check_dtype=False)
        return 1
    except:
        return 0


exec_context = r"""
import numpy as np
import pandas as pd
import torch
a, b = test_input
[insert]
result = ab
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\n    if a.shape[0] == 1:\n        ab = torch.stack((a, b), dim=0)\n    else:\n        ab = torch.cat((a, b.unsqueeze(0)), dim=0)\n'
test_execution(code)

