import numpy as np
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            number = 4
        elif test_case_id == 2:
            np.random.seed(43)
            number = np.random.randint(0, 360)
        elif test_case_id == 3:
            np.random.seed(142)
            number = np.random.randint(0, 360)
        return number

    def generate_ans(data):
        _a = data
        number = _a
        deg = np.sin(np.deg2rad(number))
        rad = np.sin(number)
        result = int(rad > deg)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert result == ans
    return 1


exec_context = r"""
import numpy as np
number = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(3):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nnumber = np.random.randint(0, 360)\nsin_degree = np.sin(np.radians(number))\nsin_radian = np.sin(number)\nif abs(sin_degree) > abs(sin_radian):\n    result = 0\nelse:\n    result = 1\n'
test_execution(code)

