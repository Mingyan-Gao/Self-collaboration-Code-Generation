import numpy as np
import copy
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import sklearn
from sklearn.datasets import make_classification


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            X, y = make_classification(random_state=42)
        return X, y

    def generate_ans(data):
        X, y = data
        pipe = Pipeline(
            [("scale", StandardScaler()), ("model", SGDClassifier(random_state=42))]
        )
        grid = GridSearchCV(
            pipe, param_grid={"model__alpha": [1e-3, 1e-2, 1e-1, 1]}, cv=5
        )
        grid.fit(X, y)
        coef = grid.best_estimator_.named_steps["model"].coef_
        return coef

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))

    return test_input, expected_result


def exec_test(result, ans):
    try:
        np.testing.assert_allclose(result, ans)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", SGDClassifier(random_state=42))
])
grid = GridSearchCV(pipe, param_grid={"model__alpha": [1e-3, 1e-2, 1e-1, 1]}, cv=5)
X, y = test_input
[insert]
result = coef
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nX = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])\ny = np.array([0, 0, 1, 1])\npipe = Pipeline([\n    ("scale", StandardScaler()),\n    ("model", SGDClassifier(random_state=42))\n])\ngrid = GridSearchCV(pipe, param_grid={"model__alpha": [1e-3, 1e-2, 1e-1, 1]}, cv=5)\ngrid.fit(X, y)\ntry:\n    coef = grid.best_estimator_.named_steps[\'model\'].coef_\nexcept AttributeError:\n    coef = None\n'
test_execution(code)

