import torch
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            t = torch.LongTensor([[1, 2], [3, 4], [5, 6], [7, 8]])
        elif test_case_id == 2:
            t = torch.LongTensor(
                [[5, 6, 7], [2, 3, 4], [1, 2, 3], [7, 8, 9], [10, 11, 12]]
            )
        return t

    def generate_ans(data):
        t = data
        result = torch.ones((t.shape[0] + 2, t.shape[1] + 2)) * -1
        result[1:-1, 1:-1] = t
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
t = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\n    top_bottom_padding = torch.full((1, t.shape[1]), -1)\n    left_right_padding = torch.full((t.shape[0] + 2, 1), -1)\n    t = t.squeeze(0)\n    t = torch.cat((top_bottom_padding, t), dim=0)\n    t = torch.cat((t, top_bottom_padding), dim=0)\n    t = torch.cat((left_right_padding, t), dim=1)\n    t = torch.cat((t, left_right_padding), dim=1)\n    result = t\n'
test_execution(code)

