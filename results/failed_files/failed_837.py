import numpy as np
import copy
import xgboost.sklearn as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            trainX = [[1], [2], [3], [4], [5]]
            trainY = [1, 2, 3, 4, 5]
            testX, testY = trainX, trainY
            paramGrid = {"subsample": [0.5, 0.8]}
            model = xgb.XGBRegressor()
            gridsearch = GridSearchCV(
                model,
                paramGrid,
                cv=TimeSeriesSplit(n_splits=2).get_n_splits([trainX, trainY]),
            )
        return gridsearch, testX, testY, trainX, trainY

    def generate_ans(data):
        gridsearch, testX, testY, trainX, trainY = data
        fit_params = {
            "early_stopping_rounds": 42,
            "eval_metric": "mae",
            "eval_set": [[testX, testY]],
        }
        gridsearch.fit(trainX, trainY, **fit_params)
        b = gridsearch.score(trainX, trainY)
        c = gridsearch.predict(trainX)
        return b, c

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        np.testing.assert_allclose(result[0], ans[0])
        np.testing.assert_allclose(result[1], ans[1])
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
import xgboost.sklearn as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit
gridsearch, testX, testY, trainX, trainY = test_input
[insert]
b = gridsearch.score(trainX, trainY)
c = gridsearch.predict(trainX)
result = (b, c)
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nimport pandas as pd\nimport xgboost.sklearn as xgb\nfrom sklearn.model_selection import GridSearchCV\nfrom sklearn.model_selection import TimeSeriesSplit\nfrom sklearn.datasets import make_regression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_absolute_error\n\n# Generate synthetic data for demonstration\nX, y = make_regression(n_samples=100, n_features=5, random_state=42)\ntrainX, testX, trainY, testY = train_test_split(X, y, test_size=0.2, random_state=42)\n\ntrainX = trainX.tolist()\ntrainY = trainY.tolist()\ntestX = testX.tolist()\ntestY = testY.tolist()\n\n# Define the XGBoost model\nmodel = xgb.XGBRegressor()\n\n# Define the parameter grid\nparam_grid = {\n    \'n_estimators\': [100, 200],\n    \'learning_rate\': [0.1, 0.01],\n    \'max_depth\': [3, 5]\n}\n\n# Define the fit_params\nfit_params = {\n    "early_stopping_rounds": 42,\n    "eval_metric": "mae",\n    "eval_set": [[np.array(testX), np.array(testY)]],\n    "verbose": False\n}\n\n# Initialize TimeSeriesSplit cross-validator\ncv = TimeSeriesSplit(n_splits=2)\n\n# Instantiate GridSearchCV\ngridsearch = GridSearchCV(\n    estimator=model,\n    param_grid=param_grid,\n    cv=cv,\n    scoring=\'neg_mean_absolute_error\',\n    n_jobs=1\n)\n\n# Fit the GridSearchCV object to the training data\ngridsearch.fit(np.array(trainX), np.array(trainY), **fit_params)\n\n# Get the best score\nb = gridsearch.best_score_\n\n# Make predictions on the test set\nc = gridsearch.predict(np.array(testX))\n'
test_execution(code)

