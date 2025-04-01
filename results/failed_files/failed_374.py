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
            eval = np.array([88, 87, 62])
        elif test_case_id == 2:
            np.random.seed(42)
            grades = (np.random.rand(50) - 0.5) * 100
            eval = np.random.randint(10, 90, (5,))
        return grades, eval

    def generate_ans(data):
        _a = data
        grades, eval = _a

        def ecdf_result(x):
            xs = np.sort(x)
            ys = np.arange(1, len(xs) + 1) / float(len(xs))
            return xs, ys

        resultx, resulty = ecdf_result(grades)
        result = np.zeros_like(eval, dtype=float)
        for i, element in enumerate(eval):
            if element < resultx[0]:
                result[i] = 0
            elif element >= resultx[-1]:
                result[i] = 1
            else:
                result[i] = resulty[(resultx > element).argmax() - 1]
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert np.allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
grades, eval = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\n\ndef ecdf(x):\n  # normalize X to sum to 1\n  x = np.sort(x)\n  n = len(x)\n  y = np.arange(1, n+1) / n\n  return x, y\n\ngrades = np.array((93.5,93,60.8,94.5,82,87.5,91.5,99.5,86,93.5,92.5,78,76,69,94.5,\n          89.5,92.8,78,65.5,98,98.5,92.3,95.5,76,91,95,61))\neval = np.array([88, 87, 62])\n\nx, y = ecdf(grades)\nresult = np.interp(eval, x, y)\n'
test_execution(code)

