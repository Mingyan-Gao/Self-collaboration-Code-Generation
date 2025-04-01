import numpy as np
import copy
from sklearn import linear_model
import sklearn
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            X_train, y_train = make_regression(
                n_samples=1000, n_features=5, random_state=42
            )
            X_train, X_test, y_train, y_test = train_test_split(
                X_train, y_train, test_size=0.4, random_state=42
            )
        return X_train, y_train, X_test, y_test

    def generate_ans(data):
        X_train, y_train, X_test, y_test = data
        ElasticNet = linear_model.ElasticNet()
        ElasticNet.fit(X_train, y_train)
        training_set_score = ElasticNet.score(X_train, y_train)
        test_set_score = ElasticNet.score(X_test, y_test)
        return training_set_score, test_set_score

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))

    return test_input, expected_result


def exec_test(result, ans):
    try:
        np.testing.assert_allclose(result, ans, rtol=1e-3)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
from sklearn import linear_model
import statsmodels.api as sm
X_train, y_train, X_test, y_test = test_input
[insert]
result = (training_set_score, test_set_score)
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nimport pandas as pd\nfrom sklearn import linear_model\nimport statsmodels.api as sm\n\ndef load_data():\n    # Replace this with your actual data loading code\n    X_train = np.array([[1, 2], [3, 4], [5, 6]])\n    y_train = np.array([7, 8, 9])\n    X_test = np.array([[11, 12], [13, 14], [15, 16]])\n    y_test = np.array([17, 18, 19])\n    return X_train, y_train, X_test, y_test\n\nX_train, y_train, X_test, y_test = load_data()\n\nassert type(X_train) == np.ndarray\nassert type(y_train) == np.ndarray\nassert type(X_test) == np.ndarray\nassert type(y_test) == np.ndarray\n\nelastic_net = linear_model.ElasticNet()\nelastic_net.fit(X_train, y_train)\n\ntraining_set_score = elastic_net.score(X_train, y_train)\ntest_set_score = elastic_net.score(X_test, y_test)\n'
test_execution(code)

