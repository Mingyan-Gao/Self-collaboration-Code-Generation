import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data

        def get_relation(df, col1, col2):
            first_max = df[[col1, col2]].groupby(col1).count().max()[0]
            second_max = df[[col1, col2]].groupby(col2).count().max()[0]
            if first_max == 1:
                if second_max == 1:
                    return "one-2-one"
                else:
                    return "one-2-many"
            else:
                if second_max == 1:
                    return "many-2-one"
                else:
                    return "many-2-many"

        result = pd.DataFrame(index=df.columns, columns=df.columns)
        for col_i in df.columns:
            for col_j in df.columns:
                if col_i == col_j:
                    continue
                result.loc[col_i, col_j] = get_relation(df, col_i, col_j)
        return result

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "Column1": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "Column2": [4, 3, 6, 8, 3, 4, 1, 4, 3],
                    "Column3": [7, 3, 3, 1, 2, 2, 3, 2, 7],
                    "Column4": [9, 8, 7, 6, 5, 4, 3, 2, 1],
                    "Column5": [1, 1, 1, 1, 1, 1, 1, 1, 1],
                }
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "Column1": [4, 3, 6, 8, 3, 4, 1, 4, 3],
                    "Column2": [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    "Column3": [7, 3, 3, 1, 2, 2, 3, 2, 7],
                    "Column4": [9, 8, 7, 6, 5, 4, 3, 2, 1],
                    "Column5": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                }
            )
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
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\n\ndef column_relationship(df):\n    cols = df.columns\n    relationship_df = pd.DataFrame(index=cols, columns=cols)\n\n    for col1 in cols:\n        for col2 in cols:\n            if col1 == col2:\n                relationship_df.loc[col1, col2] = np.nan\n            else:\n                unique_col1 = df[col1].nunique()\n                unique_col2 = df[col2].nunique()\n                unique_pairs = df.groupby([col1, col2]).size().shape[0]\n\n                if unique_col1 == unique_col2 == unique_pairs:\n                    relationship_df.loc[col1, col2] = "one-2-one"\n                elif unique_col1 == unique_pairs:\n                    relationship_df.loc[col1, col2] = "one-2-many"\n                elif unique_col2 == unique_pairs:\n                    relationship_df.loc[col1, col2] = "many-2-one"\n                else:\n                    relationship_df.loc[col1, col2] = "many-2-many"\n    return relationship_df\n\nresult = column_relationship(df)\n'
test_execution(code)

