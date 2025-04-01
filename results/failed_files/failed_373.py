import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            grades = np.array(
                (
                    93.5,
                    93,
                    60.8,
                    94.5,
                    82,
                    87.5,
                    91.5,
                    99.5,
                    86,
                    93.5,
                    92.5,
                    78,
                    76,
                    69,
                    94.5,
                    89.5,
                    92.8,
                    78,
                    65.5,
                    98,
                    98.5,
                    92.3,
                    95.5,
                    76,
                    91,
                    95,
                    61,
                )
            )
        elif test_case_id == 2:
            np.random.seed(42)
            grades = (np.random.rand(50) - 0.5) * 100
        return grades

    def generate_ans(data):
        _a = data
        grades = _a

        def ecdf_result(x):
            xs = np.sort(x)
            ys = np.arange(1, len(xs) + 1) / float(len(xs))
            return ys

        result = ecdf_result(grades)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert np.allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
grades = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\n\ndef ecdf(x):\n  x_sorted = np.sort(x)\n  cdf = np.arange(1, len(x)+1) / len(x)\n  return x_sorted, cdf\n\ngrades = np.array((93.5,93,60.8,94.5,82,87.5,91.5,99.5,86,93.5,92.5,78,76,69,94.5,\n          89.5,92.8,78,65.5,98,98.5,92.3,95.5,76,91,95,61))\n\nsorted_grades, result = ecdf(grades)\n'
test_execution(code)

