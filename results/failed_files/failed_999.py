import torch
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            torch.random.manual_seed(42)
            hid_dim = 32
            data = torch.randn(10, 2, 3, hid_dim)
            data = data.view(10, 2 * 3, hid_dim)
            W = torch.randn(hid_dim)
        return data, W

    def generate_ans(data):
        data, W = data
        W = W.unsqueeze(0).unsqueeze(0).expand(*data.size())
        result = torch.sum(data * W, 2)
        result = result.view(10, 2, 3)
        return result

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
data, W = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nW = W.unsqueeze(1)\nresult = torch.bmm(data, W).squeeze(2)\n'
test_execution(code)

