import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        someTuple = data
        return pd.DataFrame(
            np.column_stack(someTuple), columns=["birdType", "birdCount"]
        )

    def define_test_input(test_case_id):
        if test_case_id == 1:
            np.random.seed(123)
            birds = np.random.choice(
                ["African Swallow", "Dead Parrot", "Exploding Penguin"], size=int(5e4)
            )
            someTuple = np.unique(birds, return_counts=True)
        return someTuple

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
someTuple = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\nresult = pd.DataFrame(list(zip(someTuple[0], someTuple[1])), columns=['birdType', 'birdCount'])\n"
test_execution(code)

