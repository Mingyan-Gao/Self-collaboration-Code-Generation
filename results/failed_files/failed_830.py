import pandas as pd
import copy
from scipy.sparse import csr_matrix


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            df_origin = pd.DataFrame([[1, 1, 4], [0, 3, 0]], columns=["A", "B", "C"])
            transform_output = csr_matrix([[1, 0, 2], [0, 3, 0]])
        elif test_case_id == 2:
            df_origin = pd.DataFrame(
                [[1, 1, 4, 5], [1, 4, 1, 9]], columns=["A", "B", "C", "D"]
            )
            transform_output = csr_matrix([[1, 9, 8, 1, 0], [1, 1, 4, 5, 1]])
        return df_origin, transform_output

    def generate_ans(data):
        df_origin, transform_output = data
        df = pd.concat([df_origin, pd.DataFrame(transform_output.toarray())], axis=1)
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        pd.testing.assert_frame_equal(result, ans, check_dtype=False, check_names=False)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
df_origin, transform_output = test_input
def solve(df, transform_output):
[insert]
df = solve(df_origin, transform_output)
result = df
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\n    if isinstance(transform_output, csr_matrix):\n        try:\n            feature_names = [f"feature_{i}" for i in range(transform_output.shape[1])]\n            df_transformed = pd.DataFrame.sparse.from_spmatrix(transform_output, columns=feature_names)\n        except:\n            df_transformed = pd.DataFrame(transform_output.toarray())\n            df_transformed.columns = [f"feature_{i}" for i in range(df_transformed.shape[1])]\n\n    else:\n        df_transformed = pd.DataFrame(transform_output)\n        df_transformed.columns = [f"feature_{i}" for i in range(df_transformed.shape[1])]\n\n    df = pd.concat([df.reset_index(drop=True), df_transformed.reset_index(drop=True)], axis=1)\n    return df\n### END SOLUTION\n'
test_execution(code)

