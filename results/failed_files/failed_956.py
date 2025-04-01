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
def Convert(t):
[insert]
Tensor_3D = Convert(Tensor_2D)
result = Tensor_3D
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\n    result = []\n    for index, row in enumerate(t):\n        row = torch.Tensor(row)\n        diag_matrix = torch.diag(row)\n        scaled_matrix = index * diag_matrix\n        result.append(scaled_matrix)\n    return torch.stack(result)\n'
test_execution(code)

