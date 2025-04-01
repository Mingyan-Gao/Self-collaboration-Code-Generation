import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        result = pd.melt(df, value_vars=df.columns.tolist())
        cols = result.columns[:-1]
        for idx in result.index:
            t = result.loc[idx, cols]
            for i in range(len(cols)):
                result.loc[idx, cols[i]] = t[cols[-i - 1]]
        return result

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "col1": {0: "a", 1: "b", 2: "c"},
                    "col2": {0: 1, 1: 3, 2: 5},
                    "col3": {0: 2, 1: 4, 2: 6},
                    "col4": {0: 3, 1: 6, 2: 2},
                    "col5": {0: 7, 1: 2, 2: 3},
                    "col6": {0: 2, 1: 9, 2: 5},
                }
            )
            df.columns = [list("AAAAAA"), list("BBCCDD"), list("EFGHIJ")]
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "col1": {0: "a", 1: "b", 2: "c"},
                    "col2": {0: 1, 1: 3, 2: 5},
                    "col3": {0: 2, 1: 4, 2: 6},
                    "col4": {0: 3, 1: 6, 2: 2},
                    "col5": {0: 7, 1: 2, 2: 3},
                    "col6": {0: 2, 1: 9, 2: 5},
                }
            )
            df.columns = [
                list("AAAAAA"),
                list("BBBCCC"),
                list("DDEEFF"),
                list("GHIJKL"),
            ]
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

code = "\nvalue_vars = list(zip(*df.columns))\nresult = pd.melt(df, value_vars=value_vars, var_name=['variable_0', 'variable_1', 'variable_2'])\n"
test_execution(code)

