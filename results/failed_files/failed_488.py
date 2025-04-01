import numpy as np
import copy
from sklearn.preprocessing import MinMaxScaler


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array(
                [
                    [[1, 0.5, -2], [-0.5, 1, 6], [1, 1, 1]],
                    [[-2, -3, 1], [-0.5, 10, 6], [1, 1, 1]],
                ]
            )
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.rand(10, 5, 5)
        return a

    def generate_ans(data):
        _a = data
        a = _a
        scaler = MinMaxScaler()
        result = np.zeros_like(a)
        for i, arr in enumerate(a):
            a_one_column = arr.reshape(-1, 1)
            result_one_column = scaler.fit_transform(a_one_column)
            result[i, :, :] = result_one_column.reshape(arr.shape)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
from sklearn.preprocessing import MinMaxScaler
a = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\noriginal_shape = a.shape\na_reshaped = a.reshape(a.shape[0], -1)\nscaler = MinMaxScaler()\na_normalized = scaler.fit_transform(a_reshaped)\nresult = a_normalized.reshape(original_shape)\n'
test_execution(code)

