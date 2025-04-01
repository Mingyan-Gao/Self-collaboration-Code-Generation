import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return df.groupby("group").agg(
            lambda x: (
                x.head(1)
                if x.dtype == "object"
                else x.mean() if x.name.endswith("2") else x.sum()
            )
        )

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "group": ["A", "A", "A", "B", "B"],
                    "group_color": ["green", "green", "green", "blue", "blue"],
                    "val1": [5, 2, 3, 4, 5],
                    "val2": [4, 2, 8, 5, 7],
                    "val42": [1, 1, 4, 5, 1],
                }
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "group": ["A", "A", "A", "B", "B"],
                    "group_color": ["green", "green", "green", "blue", "blue"],
                    "val1": [5, 2, 3, 4, 5],
                    "val2": [4, 2, 8, 5, 7],
                    "val332": [1, 1, 4, 5, 1],
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

code = "\nimport pandas as pd\n\ndf = pd.DataFrame({ 'group': ['A', 'A', 'A', 'B', 'B'], 'group_color' : ['green', 'green', 'green', 'blue', 'blue'], 'val1': [5, 2, 3, 4, 5], 'val2' : [4, 2, 8, 5, 7],'val42':[1,1,4,5,1] })\n\nvalue_cols = [col for col in df.columns if 'group' not in col and 'group_color' not in col]\nagg_dict = {}\nfor col in value_cols:\n    if col.endswith('2'):\n        agg_dict[col] = 'mean'\n    else:\n        agg_dict[col] = 'sum'\nagg_dict['group_color'] = 'first'\n\nresult = df.groupby('group').agg(agg_dict)\n"
test_execution(code)

