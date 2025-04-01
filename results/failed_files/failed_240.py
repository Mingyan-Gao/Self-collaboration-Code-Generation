import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        data = data
        C, D = data
        return (
            pd.concat([C, D])
            .drop_duplicates("A", keep="last")
            .sort_values(by=["A"])
            .reset_index(drop=True)
        )

    def define_test_input(test_case_id):
        if test_case_id == 1:
            C = pd.DataFrame({"A": ["AB", "CD", "EF"], "B": [1, 2, 3]})
            D = pd.DataFrame({"A": ["CD", "GH"], "B": [4, 5]})
        if test_case_id == 2:
            D = pd.DataFrame({"A": ["AB", "CD", "EF"], "B": [1, 2, 3]})
            C = pd.DataFrame({"A": ["CD", "GH"], "B": [4, 5]})
        return C, D

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
C, D = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\nresult = pd.merge(C, D, on='A', how='left', suffixes=('_x', '_y'))\nresult['B'] = result['B_y'].fillna(result['B_x'])\nresult = result.drop(['B_x', 'B_y'], axis=1)\nresult = pd.concat([result, D[~D['A'].isin(C['A'])]], ignore_index=True)\nresult = result.fillna(0)\n"
test_execution(code)

