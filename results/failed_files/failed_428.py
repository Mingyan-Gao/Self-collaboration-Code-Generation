import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array([0, 1, 2, 5, 6, 7, 8, 8, 8, 10, 29, 32, 45])
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.randn(30)
        return a

    def generate_ans(data):
        _a = data
        a = _a
        result = (a.mean() - 3 * a.std(), a.mean() + 3 * a.std())
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
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

code = '\nimport numpy as np\na = np.array([0, 1, 2, 5, 6, 7, 8, 8, 8, 10, 29, 32, 45])\nmean = np.mean(a)\nstd = np.std(a)\nlower_bound = mean - 3 * std\nupper_bound = mean + 3 * std\nresult = (lower_bound, upper_bound)\n'
test_execution(code)

