import torch
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            torch.random.manual_seed(42)
            images = torch.randn(5, 3, 4, 4)
            labels = torch.LongTensor(5, 4, 4).random_(3)
        return images, labels

    def generate_ans(data):
        images, labels = data
        loss_func = torch.nn.CrossEntropyLoss()
        loss = loss_func(images, labels)
        return loss

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
import torch.nn.functional as F
from torch.autograd import Variable
images, labels = test_input
[insert]
result = loss
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\ndef cross_entropy2d(input, target, weight=None, size_average=True):\n    n, c, h, w = input.size()\n\n    log_p = F.log_softmax(input, dim=1)\n    target_onehot = F.one_hot(target, num_classes=c).permute(0, 3, 1, 2).float()\n    loss = -torch.sum(target_onehot * log_p) / (n * h * w)\n\n    return loss\n\nimages = Variable(torch.randn(5, 3, 4, 4))\nlabels = Variable(torch.LongTensor(5, 4, 4).random_(3))\nloss = cross_entropy2d(images, labels)\n'
test_execution(code)

