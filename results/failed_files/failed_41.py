import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        s = ""
        for c in df.columns:
            s += "---- %s ---" % c
            s += "\n"
            s += str(df[c].value_counts())
            s += "\n"
        return s

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                data=[[34, "null", "mark"], [22, "null", "mark"], [34, "null", "mark"]],
                columns=["id", "temp", "name"],
                index=[1, 2, 3],
            )
        elif test_case_id == 2:
            df = pd.DataFrame(
                data=[[11, "null", "mark"], [14, "null", "mark"], [51, "null", "mark"]],
                columns=["id", "temp", "name"],
                index=[1, 2, 3],
            )
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        assert result == ans
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

code = "\nresult = ''\nfor col in df.columns:\n    result += f'---- {col} ---\\n'\n    result += df[col].value_counts().to_string() + '\\n'\n    result += f'Name: {col}, dtype: {df[col].dtype}\\n'\n"
test_execution(code)

