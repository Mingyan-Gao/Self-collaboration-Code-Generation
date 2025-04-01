import numpy as np
import copy
import scipy.stats as ss


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            x1 = [38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0]
            x2 = [39.2, 39.3, 39.7, 41.4, 41.8, 42.9, 43.3, 45.8]
        elif test_case_id == 2:
            np.random.seed(42)
            x1, x2 = np.random.randn(2, 20)
        elif test_case_id == 3:
            np.random.seed(20)
            x1 = np.random.randn(10)
            x2 = np.random.normal(4, 5, size=(10,))
        return x1, x2

    def generate_ans(data):
        _a = data
        x1, x2 = _a
        s, c_v, s_l = ss.anderson_ksamp([x1, x2])
        result = c_v[2] >= s
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert result == ans
    return 1


exec_context = r"""
import numpy as np
import scipy.stats as ss
x1, x2 = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(3):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nimport scipy.stats as ss\nx1=np.array([38.7,  41.5,  43.8,  44.5,  45.5,  46.0,  47.7,  58.0])\nx2=np.array([39.2,  39.3,  39.7,  41.4,  41.8,  42.9,  43.3,  45.8])\nanderson_result = ss.anderson_ksamp([x1, x2])\np_value = anderson_result.significance_level\nresult = p_value > 0.05\n'
test_execution(code)

