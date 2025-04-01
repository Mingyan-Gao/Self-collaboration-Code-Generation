import numpy as np
import pandas as pd
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = np.arange(-5.5, 10.5)
            percentile = 50
        elif test_case_id == 2:
            np.random.seed(42)
            a = np.random.rand(50) - 0.5
            percentile = np.random.randint(1, 100)
        return a, percentile

    def generate_ans(data):
        _a = data
        DataArray, percentile = _a
        mdata = np.ma.masked_where(DataArray < 0, DataArray)
        mdata = np.ma.filled(mdata, np.nan)
        prob = np.nanpercentile(mdata, percentile)
        return prob

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
DataArray, percentile = test_input
[insert]
result = prob
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nDataArray = np.arange(-5.5, 10.5)\npercentile = 50\nimport numpy.ma as ma\nmasked_data = ma.masked_where(DataArray < 0, DataArray)\nprob = np.percentile(masked_data.compressed(), percentile)\n'
test_execution(code)

