import numpy as np
import pandas as pd
import copy
from sklearn.datasets import load_iris


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            data = load_iris()
        return data

    def generate_ans(data):
        data = data
        data1 = pd.DataFrame(
            data=np.c_[data["data"], data["target"]],
            columns=data["feature_names"] + ["target"],
        )
        return data1

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        for c in ans.columns:
            pd.testing.assert_series_equal(result[c], ans[c], check_dtype=False)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
data = test_input
[insert]
result = data1
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nfrom sklearn.datasets import load_iris\nimport pandas as pd\ndata = load_iris()\ndata1 = pd.DataFrame(data=data.data, columns=data.feature_names)\n'
test_execution(code)

