import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        df = df[sorted(df.columns.to_list())]
        df.columns = pd.MultiIndex.from_tuples(
            df.columns, names=["Caps", "Middle", "Lower"]
        )
        return df

    def define_test_input(test_case_id):
        if test_case_id == 1:
            l = [
                ("A", "a", "1"),
                ("A", "b", "2"),
                ("B", "a", "1"),
                ("A", "b", "1"),
                ("B", "b", "1"),
                ("A", "a", "2"),
            ]
            np.random.seed(1)
            df = pd.DataFrame(np.random.randn(5, 6), columns=l)
        return df

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
df = test_input
[insert]
result = df
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\ncaps = pd.unique([c[0] for c in df.columns])\nmiddle = pd.unique([c[1] for c in df.columns])\nlower = pd.unique([c[2] for c in df.columns])\n\nnew_cols = pd.MultiIndex.from_tuples(df.columns)\ndf.columns = new_cols\n'
test_execution(code)

