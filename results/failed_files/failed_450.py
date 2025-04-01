import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            np.random.seed(42)
            a = np.random.rand(5, 5, 5)
            second = [1, 2]
            third = [3, 4]
        elif test_case_id == 2:
            np.random.seed(45)
            a = np.random.rand(7, 8, 9)
            second = [0, 4]
            third = [6, 7]
        return a, second, third

    def generate_ans(data):
        _a = data
        a, second, third = _a
        result = a[:, np.array(second).reshape(-1, 1), third]
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
a, second, third = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nresult = a[:, second, third]\n'
test_execution(code)

