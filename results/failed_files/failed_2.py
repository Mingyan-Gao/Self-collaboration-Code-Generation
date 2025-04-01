import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return df.where(df.apply(lambda x: x.map(x.value_counts())) >= 2, "other")

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

code = "\nfor col in ['Qu1', 'Qu3']:\n    counts = df[col].value_counts()\n    infrequent_values = counts[counts < 2].index\n    df[col] = df[col].replace(infrequent_values, 'other')\n\nresult = df\n"
test_execution(code)

