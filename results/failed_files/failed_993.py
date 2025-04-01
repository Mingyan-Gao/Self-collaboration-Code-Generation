import torch
import copy
import sklearn
from sklearn.datasets import load_iris


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            X, y = load_iris(return_X_y=True)
            input = torch.from_numpy(X[42]).float()
            torch.manual_seed(42)
            MyNet = torch.nn.Sequential(
                torch.nn.Linear(4, 15),
                torch.nn.Sigmoid(),
                torch.nn.Linear(15, 3),
            )
            torch.save(MyNet.state_dict(), "my_model.pt")
        return input

    def generate_ans(data):
        input = data
        MyNet = torch.nn.Sequential(
            torch.nn.Linear(4, 15),
            torch.nn.Sigmoid(),
            torch.nn.Linear(15, 3),
        )
        MyNet.load_state_dict(torch.load("my_model.pt"))
        output = MyNet(input)
        probs = torch.nn.functional.softmax(output.reshape(1, 3), dim=1)
        confidence_score, classes = torch.max(probs, 1)
        return confidence_score

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
MyNet = torch.nn.Sequential(torch.nn.Linear(4, 15),
                            torch.nn.Sigmoid(),
                            torch.nn.Linear(15, 3),
                            )
MyNet.load_state_dict(torch.load("my_model.pt"))
input = test_input
[insert]
result = confidence_score
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport torch\nimport torch.nn.functional as F\nMyNet = torch.nn.Sequential(torch.nn.Linear(4, 15),\n                            torch.nn.Sigmoid(),\n                            torch.nn.Linear(15, 3),\n                            )\nMyNet.load_state_dict(torch.load("my_model.pt"))\nMyNet.eval()\nwith torch.no_grad():\n    output = MyNet(input)\n    probabilities = F.softmax(output, dim=1)\n    confidence_score = torch.max(probabilities).item()\n'
test_execution(code)

