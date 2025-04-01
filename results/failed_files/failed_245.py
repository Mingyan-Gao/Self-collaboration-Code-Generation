import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return (
            df.groupby("user")[["time", "amount"]]
            .apply(lambda x: x.values.tolist()[::-1])
            .to_frame(name="amount-time-tuple")
        )

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                {
                    "user": [1, 1, 2, 2, 3],
                    "time": [20, 10, 11, 18, 15],
                    "amount": [10.99, 4.99, 2.99, 1.99, 10.99],
                }
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                {
                    "user": [1, 1, 1, 2, 2, 3],
                    "time": [20, 10, 30, 11, 18, 15],
                    "amount": [10.99, 4.99, 16.99, 2.99, 1.99, 10.99],
                }
            )
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        pd.testing.assert_frame_equal(result, ans)
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

code = "\ndf['amount-time-tuple'] = list(zip(df['time'], df['amount']))\nresult = df.groupby('user')['amount-time-tuple'].apply(lambda x: sorted(x, reverse=True))\n"
test_execution(code)

