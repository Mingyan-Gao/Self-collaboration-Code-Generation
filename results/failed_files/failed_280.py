import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        corr = data
        corr_triu = corr.where(~np.tril(np.ones(corr.shape)).astype(bool))
        corr_triu = corr_triu.stack()
        corr_triu.name = "Pearson Correlation Coefficient"
        corr_triu.index.names = ["Col1", "Col2"]
        return corr_triu[corr_triu > 0.3].to_frame()

    def define_test_input(test_case_id):
        if test_case_id == 1:
            np.random.seed(10)
            df = pd.DataFrame(np.random.rand(10, 5))
            corr = df.corr()
        return corr

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        pd.testing.assert_frame_equal(result, ans, check_dtype=False)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
corr = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\ncorr_unstacked = corr.stack()\nfiltered_corr = corr_unstacked[corr_unstacked > 0.3]\nresult = pd.DataFrame(filtered_corr, columns=['Pearson Correlation Coefficient']).rename_axis(['Col1', 'Col2'])\n"
test_execution(code)

