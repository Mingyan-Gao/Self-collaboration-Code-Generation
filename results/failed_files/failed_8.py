import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return df.loc[(df["drop_if_dup"] == "No") | ~df["url"].duplicated()]

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "url": [
                        "A.com",
                        "A.com",
                        "A.com",
                        "B.com",
                        "B.com",
                        "C.com",
                        "B.com",
                    ],
                    "drop_if_dup": ["Yes", "Yes", "No", "No", "No", "No", "Yes"],
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
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\nseen_urls = set()\nresult = []\nfor index, row in df.iterrows():\n    if row['url'] not in seen_urls:\n        result.append(row)\n        if row['drop_if_dup'] == 'Yes':\n            seen_urls.add(row['url'])\n    elif row['drop_if_dup'] == 'No':\n        result.append(row)\nresult = pd.DataFrame(result)\n"
test_execution(code)

