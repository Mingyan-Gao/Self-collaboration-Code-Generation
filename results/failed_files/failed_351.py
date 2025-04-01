import numpy as np
import copy
import scipy.stats


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            np.random.seed(42)
            a = np.random.randn(40)
            b = 4 * np.random.randn(50)
        elif test_case_id == 2:
            np.random.seed(43)
            a = np.random.randn(40)
            b = 4 * np.random.randn(50)
            a[10] = np.nan
            b[20] = np.nan
        return a, b

    def generate_ans(data):
        _a = data
        a, b = _a
        _, p_value = scipy.stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
        return p_value

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert abs(ans - result) <= 1e-5
    return 1


exec_context = r"""
import numpy as np
import scipy.stats
a, b = test_input
[insert]
result = p_value
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\na = a[~np.isnan(a)]\nb = b[~np.isnan(b)]\nn_a = len(a)\nn_b = len(b)\nif n_a > 1 and n_b > 1:\n    mean_a = np.mean(a)\n    mean_b = np.mean(b)\n    var_a = np.var(a, ddof=1)\n    var_b = np.var(b, ddof=1)\n    pooled_variance = ((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2)\n    t_statistic = (mean_a - mean_b) / np.sqrt(pooled_variance * (1/n_a + 1/n_b))\n    degrees_of_freedom = n_a + n_b - 2\n    p_value = scipy.stats.t.sf(np.abs(t_statistic), degrees_of_freedom) * 2\nelse:\n    p_value = np.nan\n'
test_execution(code)

