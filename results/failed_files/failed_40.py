import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return df.apply(lambda x: x.value_counts()).T.null

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                data=[[34, "null", "null"], [22, "null", "mark"], [34, "null", "mark"]],
                columns=["id", "temp", "name"],
                index=[1, 2, 3],
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                data=[[34, "null", "null"], [22, "null", "mark"], [34, "null", "null"]],
                columns=["id", "temp", "name"],
                index=[1, 2, 3],
            )
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        pd.testing.assert_series_equal(result, ans)
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

code = "\nresult = df.apply(lambda x: x.astype(str).str.contains('null').sum())\nresult.name = 'null'\n"
test_execution(code)

