import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        for col in df.columns:
            vc = df[col].value_counts()
            if col == "Qu1":
                df[col] = df[col].apply(lambda x: x if vc[x] >= 3 else "other")
            else:
                df[col] = df[col].apply(lambda x: x if vc[x] >= 2 else "other")
        return df

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "Qu1": [
                        "apple",
                        "potato",
                        "cheese",
                        "banana",
                        "cheese",
                        "banana",
                        "cheese",
                        "potato",
                        "egg",
                    ],
                    "Qu2": [
                        "sausage",
                        "banana",
                        "apple",
                        "apple",
                        "apple",
                        "sausage",
                        "banana",
                        "banana",
                        "banana",
                    ],
                    "Qu3": [
                        "apple",
                        "potato",
                        "sausage",
                        "cheese",
                        "cheese",
                        "potato",
                        "cheese",
                        "potato",
                        "egg",
                    ],
                }
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "Qu1": [
                        "sausage",
                        "banana",
                        "apple",
                        "apple",
                        "apple",
                        "sausage",
                        "banana",
                        "banana",
                        "banana",
                    ],
                    "Qu2": [
                        "apple",
                        "potato",
                        "sausage",
                        "cheese",
                        "cheese",
                        "potato",
                        "cheese",
                        "potato",
                        "egg",
                    ],
                    "Qu3": [
                        "apple",
                        "potato",
                        "cheese",
                        "banana",
                        "cheese",
                        "banana",
                        "cheese",
                        "potato",
                        "egg",
                    ],
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

code = "\ndef transform_column(df, column_name, min_count):\n    value_counts = df[column_name].value_counts()\n    to_replace = value_counts[value_counts < min_count].index\n    df[column_name] = df[column_name].replace(to_replace, 'other')\n    return df\n\ndf = transform_column(df, 'Qu1', 3)\ndf = transform_column(df, 'Qu3', 2)\n\nresult = df\n"
test_execution(code)

