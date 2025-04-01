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
            threshold = 0.5
        elif test_case_id == 2:
            np.random.seed(42)
            grades = (np.random.rand(50) - 0.5) * 100
            threshold = 0.6
        return grades, threshold

    def generate_ans(data):
        _a = data
        grades, threshold = _a

        def ecdf_result(x):
            xs = np.sort(x)
            ys = np.arange(1, len(xs) + 1) / float(len(xs))
            return xs, ys

        resultx, resulty = ecdf_result(grades)
        t = (resulty > threshold).argmax()
        low = resultx[0]
        high = resultx[t]
        return [low, high]

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
grades, threshold = test_input
[insert]
result = [low, high]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\n\ndef ecdf(x):\n    x = np.sort(x)\n    n = len(x)\n    if n == 0:\n        return np.array([])\n    return np.arange(1, n + 1) / n\n\ngrades = np.array((93.5,93,60.8,94.5,82,87.5,91.5,99.5,86,93.5,92.5,78,76,69,94.5,\n          89.5,92.8,78,65.5,98,98.5,92.3,95.5,76,91,95,61))\nthreshold = 0.5\n\nlongest_interval = (None, None)\nmax_length = 0\n\nfor i in range(len(grades)):\n    for j in range(i, len(grades)):\n        low_val = grades[i]\n        high_val = grades[j]\n        interval = grades[(grades >= low_val) & (grades <= high_val)]\n        \n        if len(interval) > 0:\n            ecdf_values = ecdf(grades[grades <= high_val])\n            \n            valid_interval = True\n            for val in interval:\n                ecdf_index = np.where(np.sort(grades) == val)[0][0]\n                ecdf_value = ecdf(grades)[ecdf_index]\n                if ecdf_value >= threshold:\n                    valid_interval = False\n                    break\n            \n            if valid_interval:\n                current_length = high_val - low_val\n                if current_length > max_length:\n                    max_length = current_length\n                    longest_interval = (low_val, high_val)\n\nif longest_interval == (None, None):\n    low, high = None, None\nelse:\n    low, high = longest_interval[0], longest_interval[1]\n'
test_execution(code)

