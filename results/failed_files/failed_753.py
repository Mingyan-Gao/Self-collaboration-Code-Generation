import numpy as np
import copy
import scipy.stats as ss


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            x1 = [38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0]
            x2 = [39.2, 39.3, 39.7, 41.4, 41.8, 42.9, 43.3, 45.8]
            x3 = [34.0, 35.0, 39.0, 40.0, 43.0, 43.0, 44.0, 45.0]
            x4 = [34.0, 34.8, 34.8, 35.4, 37.2, 37.8, 41.2, 42.8]
        elif test_case_id == 2:
            np.random.seed(42)
            x1, x2, x3, x4 = np.random.randn(4, 20)
        return x1, x2, x3, x4

    def generate_ans(data):
        _a = data
        x1, x2, x3, x4 = _a
        statistic, critical_values, significance_level = ss.anderson_ksamp(
            [x1, x2, x3, x4]
        )
        return [statistic, critical_values, significance_level]

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert abs(result[0] - ans[0]) <= 1e-5
    assert np.allclose(result[1], ans[1])
    assert abs(result[2] - ans[2]) <= 1e-5
    return 1


exec_context = r"""
import numpy as np
import scipy.stats as ss
x1, x2, x3, x4 = test_input
[insert]
result = [statistic, critical_values, significance_level]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nimport scipy.stats as ss\nx1=[38.7,  41.5,  43.8,  44.5,  45.5,  46.0,  47.7,  58.0]\nx2=[39.2,  39.3,  39.7,  41.4,  41.8,  42.9,  43.3,  45.8]\nx3=[34.0,  35.0,  39.0,  40.0,  43.0,  43.0,  44.0,  45.0]\nx4=[34.0,  34.8,  34.8,  35.4,  37.2,  37.8,  41.2,  42.8]\nstatistic, critical_values, significance_level = ss.anderson_ksamp([x1, x2, x3, x4])\n'
test_execution(code)

