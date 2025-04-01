import numpy as np
import copy
from sklearn.preprocessing import StandardScaler


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            data = [[1, 1], [2, 3], [3, 2], [1, 1]]
        return data

    def generate_ans(data):
        data = data
        scaler = StandardScaler()
        scaler.fit(data)
        scaled = scaler.transform(data)
        inversed = scaler.inverse_transform(scaled)
        return inversed

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
from sklearn.preprocessing import StandardScaler
data = test_input
scaler = StandardScaler()
scaler.fit(data)
scaled = scaler.transform(data)
def solve(data, scaler, scaled):
[insert]
inversed = solve(data, scaler, scaled)
result = inversed
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\n    from sklearn.linear_model import LinearRegression\n    from sklearn.model_selection import train_test_split\n    \n    X = data.drop('t', axis=1)\n    y = data['t']\n    \n    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n    \n    scaler = StandardScaler()\n    y_train_scaled = scaler.fit_transform(y_train.values.reshape(-1, 1))\n    y_test_scaled = scaler.transform(y_test.values.reshape(-1, 1))\n    \n    model = LinearRegression()\n    model.fit(X_train, y_train_scaled)\n    \n    y_pred_scaled = model.predict(X_test)\n    \n    y_pred = scaler.inverse_transform(y_pred_scaled.reshape(-1, 1))\n    \n    return y_pred\n### END SOLUTION\n"
test_execution(code)

