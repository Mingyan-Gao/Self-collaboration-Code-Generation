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
            param_group["lr"] = 0.0005
        return optim

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        assert ans.defaults == result.defaults
        for param_group in result.param_groups:
            assert param_group["lr"] == 0.0005
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

code = '\nimport torch\nimport torch.optim as optim\n\ndef load_data():\n    # Dummy parameters for demonstration\n    params = [torch.nn.Parameter(torch.randn(2, 3))]\n    optimizer = optim.SGD(params, lr=0.005)\n    return optimizer\n\ndef update_lr(optimizer, new_lr):\n    for param_group in optimizer.param_groups:\n        param_group[\'lr\'] = new_lr\n\noptim = load_data()\n\n# Simulate training loop\nloss = 0.1\nprint(f"Initial learning rate: {optim.param_groups[0][\'lr\']}")\nprint(f"Initial loss: {loss}")\n\n# Simulate loss increase\nloss = 0.2\nprint(f"Loss increased to: {loss}")\n\n# Update learning rate\nupdate_lr(optim, 0.0005)\nprint(f"Updated learning rate: {optim.param_groups[0][\'lr\']}")\n\n# Guidance on choosing learning rate:\nprint("\\nGuidance on choosing between lr=0.05 and lr=0.0005:")\nprint("If the loss increase is significant and you are in the early stages of training, a larger decrease (e.g., from 0.05 to 0.0005) might be appropriate.")\nprint("If the loss increase is small or you are nearing convergence, a smaller decrease would be better to avoid drastic changes to the training process.")\n'
test_execution(code)

