import pandas as pd
import numpy as np
import yaml
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        df.message = df.message.replace(["\[", "\]"], ["{", "}"], regex=True).apply(
            yaml.safe_load
        )
        df1 = pd.DataFrame(df.pop("message").values.tolist(), index=df.index)
        result = pd.concat([df, df1], axis=1)
        result = result.replace("", "none")
        result = result.replace(np.nan, "none")
        return result

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "name": ["matt", "james", "adam"],
                    "status": ["active", "active", "inactive"],
                    "number": [12345, 23456, 34567],
                    "message": [
                        "[job:  , money: none, wife: none]",
                        "[group: band, wife: yes, money: 10000]",
                        "[job: none, money: none, wife:  , kids: one, group: jail]",
                    ],
                }
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "name": ["matt", "james", "adam"],
                    "status": ["active", "active", "inactive"],
                    "number": [12345, 23456, 34567],
                    "message": [
                        "[job:  , money: 114514, wife: none, kids: one, group: jail]",
                        "[group: band, wife: yes, money: 10000]",
                        "[job: none, money: none, wife:  , kids: one, group: jail]",
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

code = "\ndef parse_message(message):\n    message = message.strip('[]')\n    pairs = message.split(',')\n    result = {}\n    for pair in pairs:\n        if ':' in pair:\n            key, value = pair.split(':', 1)\n            key = key.strip()\n            value = value.strip()\n            if key:\n                result[key] = value if value else 'none'\n    return result\n\ndf['parsed_message'] = df['message'].apply(parse_message)\ndf = pd.concat([df, df['parsed_message'].apply(pd.Series)], axis=1)\ndf = df.fillna('none')\ndf = df.drop(['message', 'parsed_message'], axis=1)\nresult = df\n"
test_execution(code)

