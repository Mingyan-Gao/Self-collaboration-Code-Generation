import numpy as np
import copy
import sklearn
from sklearn.preprocessing import MultiLabelBinarizer


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            features = [["f1", "f2", "f3"], ["f2", "f4", "f5", "f6"], ["f1", "f2"]]
        return features

    def generate_ans(data):
        features = data
        new_features = MultiLabelBinarizer().fit_transform(features)
        rows, cols = new_features.shape
        for i in range(rows):
            for j in range(cols):
                if new_features[i, j] == 1:
                    new_features[i, j] = 0
                else:
                    new_features[i, j] = 1
        return new_features

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))

    return test_input, expected_result


def exec_test(result, ans):
    try:
        np.testing.assert_equal(result, ans)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
import sklearn
features = test_input
[insert]
result = new_features
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\n    unique_features = set()\n    for sample in features:\n        unique_features.update(sample)\n    \n    feature_to_index = {feature: i for i, feature in enumerate(unique_features)}\n    \n    new_features = np.zeros((len(features), len(unique_features)), dtype=int)\n    \n    for i, sample in enumerate(features):\n        for feature in sample:\n            new_features[i, feature_to_index[feature]] = 1\n'
test_execution(code)

