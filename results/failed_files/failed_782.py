import numpy as np
import copy
from scipy.spatial import distance


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            shape = (6, 6)
        elif test_case_id == 2:
            shape = (10, 3)
        elif test_case_id == 3:
            np.random.seed(42)
            shape = np.random.randint(2, 15, (2,))
        return shape

    def generate_ans(data):
        _a = data
        shape = _a
        xs, ys = np.indices(shape)
        xs = xs.reshape(shape[0] * shape[1], 1)
        ys = ys.reshape(shape[0] * shape[1], 1)
        X = np.hstack((xs, ys))
        mid_x, mid_y = (shape[0] - 1) / 2.0, (shape[1] - 1) / 2.0
        result = distance.cdist(X, np.atleast_2d([mid_x, mid_y])).reshape(shape)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert np.allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
from scipy.spatial import distance
shape = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(3):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nrows, cols = shape\ny, x = np.indices(shape)\ncenter_y, center_x = rows / 2, cols / 2\ncoords = np.dstack((y, x)).reshape(-1, 2)\ncenter = np.array([[center_y, center_x]])\nresult = distance.cdist(coords, center).reshape(shape)\n'
test_execution(code)

