import pandas as pd
import copy
import sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            data, target = load_iris(as_frame=True, return_X_y=True)
            dataset = pd.concat([data, target], axis=1)
        elif test_case_id == 2:
            data, target = load_iris(as_frame=True, return_X_y=True)
            dataset = pd.concat([data.iloc[:, :-1], target], axis=1)
        return dataset

    def generate_ans(data):
        dataset = data
        x_train, x_test, y_train, y_test = train_test_split(
            dataset.iloc[:, :-1], dataset.iloc[:, -1], test_size=0.2, random_state=42
        )
        return x_train, x_test, y_train, y_test

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))

    return test_input, expected_result


def exec_test(result, ans):
    try:
        pd.testing.assert_frame_equal(result[0], ans[0])
        pd.testing.assert_frame_equal(result[1], ans[1])
        pd.testing.assert_series_equal(result[2], ans[2])
        pd.testing.assert_series_equal(result[3], ans[3])
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
dataset = test_input
def solve(data):
[insert]
x_train, y_train, x_test, y_test = solve(dataset)
result = x_train, x_test, y_train, y_test
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\n\ndef solve(data):\n    # Split the data into training and testing sets\n    train, test = train_test_split(data, test_size=0.2, random_state=42)\n    \n    # Split the training set into features (X_train) and target (Y_train)\n    x_train = train.iloc[:, :-1]\n    y_train = train.iloc[:, -1]\n    \n    # Split the testing set into features (X_test) and target (Y_test)\n    x_test = test.iloc[:, :-1]\n    y_test = test.iloc[:, -1]\n    \n    return x_train, y_train, x_test, y_test\n### END SOLUTION\n'
test_execution(code)

