import numpy as np
import pandas as pd
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame({"a": [1, "foo", "bar"]})
            target = "f"
            choices = ["XX"]
        return df, target, choices

    def generate_ans(data):
        _a = data
        df, target, choices = _a
        conds = df.a.str.contains(target, na=False)
        result = np.select([conds], choices, default=np.nan)
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
import pandas as pd
df, target, choices = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)


def test_string(solution: str):
    tokens = []
    for token in tokenize.tokenize(io.BytesIO(solution.encode("utf-8")).readline):
        tokens.append(token.string)
    assert "select" in tokens and "np" in tokens

code = '\nimport numpy as np\nimport pandas as pd\n\ndf = pd.DataFrame({\'properties_path\': [\'/za/\', \'/en/\', \'blog/article\', \'credit-card-readers/\', \'signup\', \'complete\', \'promo\', np.nan]})\n\nconditions = [\n    df["properties_path"].str.contains(\'blog\', na=False),\n    df["properties_path"].str.contains(\'credit-card-readers/|machines|poss|team|transaction_fees\', na=False),\n    df["properties_path"].str.contains(\'signup|sign-up|create-account|continue|checkout\', na=False),\n    df["properties_path"].str.contains(\'complete\', na=False),\n    df["properties_path"] == \'/za/\',\n    df["properties_path"].str.contains(\'promo\', na=False)\n]\n\nchoices = ["blog", "info_pages", "signup", "completed", "home_page", "promo"]\n\ndf["page_type"] = np.select(conditions, choices, default=np.nan)\nresult = df\n'
test_execution(code)
test_string(code)
