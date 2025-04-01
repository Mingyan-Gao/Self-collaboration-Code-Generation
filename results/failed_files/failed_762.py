import numpy as np
import copy
import scipy.stats


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.array([1.0, 2.0, 2.5, 400.0, 6.0, 0.0])
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.randn(10)
        return a

    def generate_ans(data):
        _a = data
        a = _a
        kurtosis_result = scipy.stats.kurtosis(a)
        return kurtosis_result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert np.allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
import scipy.stats
a = test_input
[insert]
result = kurtosis_result
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\n    mean = np.mean(a)\n    std = np.std(a)\n    fourth_moment = np.sum((a - mean)**4) / len(a)\n    kurtosis = fourth_moment / (std**4) - 3\n    kurtosis_result = kurtosis\n'
test_execution(code)

