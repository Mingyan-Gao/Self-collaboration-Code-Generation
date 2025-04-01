import torch
import copy
from torch import nn


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:

            class MyAttentionBiLSTM(nn.Module):
                def __init__(self):
                    super(MyAttentionBiLSTM, self).__init__()
                    self.lstm = nn.LSTM(
                        input_size=20,
                        hidden_size=20,
                        num_layers=1,
                        batch_first=True,
                        bidirectional=True,
                    )
                    self.attentionW = nn.Parameter(torch.randn(5, 20 * 2))
                    self.softmax = nn.Softmax(dim=1)
                    self.linear = nn.Linear(20 * 2, 2)

            model = MyAttentionBiLSTM()
            optim = torch.optim.SGD(
                [{"params": model.lstm.parameters()}, {"params": model.attentionW}],
                lr=0.01,
            )
        return optim

    def generate_ans(data):
        optim = data
        for param_group in optim.param_groups:
            param_group["lr"] = 0.001
        return optim

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        assert ans.defaults == result.defaults
        for param_group in result.param_groups:
            assert param_group["lr"] == 0.001
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
import torch
optim = test_input
[insert]
result = optim
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport torch\n\n# Initialize optimizer\noptimizer = torch.optim.SGD([torch.randn(10, requires_grad=True)], lr=0.01)\n\n# Initial learning rate\ninitial_lr = optimizer.param_groups[0][\'lr\']\nprint(f"Initial learning rate: {initial_lr}")\n\n# Simulate training loop\nprevious_loss = float(\'inf\')\nfor epoch in range(5):\n    # Simulate loss calculation\n    loss = torch.rand(1)\n\n    print(f"Epoch {epoch+1}, Loss: {loss.item()}")\n\n    # Check if loss increased\n    if loss > previous_loss:\n        print("Loss increased, updating learning rate")\n        # Update learning rate\n        for param_group in optimizer.param_groups:\n            param_group[\'lr\'] = 0.001\n        \n        # Print updated learning rate\n        print(f"New learning rate: {optimizer.param_groups[0][\'lr\']}")\n\n    # Store current loss for next iteration\n    previous_loss = loss\n'
test_execution(code)

