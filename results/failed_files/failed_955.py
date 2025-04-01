import torch
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        torch.random.manual_seed(42)
        if test_case_id == 1:
            a = torch.rand(2, 3)
        elif test_case_id == 2:
            a = torch.rand(4, 5)
        return a

    def generate_ans(data):
        a = data
        Tensor_3D = torch.diag_embed(a)
        return Tensor_3D

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
Tensor_2D = test_input
[insert]
result = Tensor_3D
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\n    batch_size = Tensor_2D.shape[0]\n    diag_len = Tensor_2D.shape[1]\n    Tensor_3D = torch.zeros(batch_size, diag_len, diag_len)\n    for i in range(batch_size):\n        Tensor_3D[i] = torch.diag(Tensor_2D[i])\n'
test_execution(code)

