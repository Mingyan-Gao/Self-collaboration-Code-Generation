def generate_test_case(test_case_id):
    return None, None


def exec_test(result, ans):
    try:
        assert len(result[0]) > 1 and len(result[1]) > 1
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
X = [['asdf', '1'], ['asdf', '0']]
clf = DecisionTreeClassifier()
[insert]
clf.fit(new_X, ['2', '3'])
result = new_X
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.preprocessing import OneHotEncoder\nimport numpy as np\n\nnew_X = [['asdf', '1'], ['asdf', '0'], ['qwer', '1']]\nenc = OneHotEncoder(handle_unknown='ignore')\nenc.fit(new_X)\nencoded_X = enc.transform(new_X).toarray()\nclf = DecisionTreeClassifier()\ny = ['2', '3', '4']\nclf.fit(encoded_X, y)\n"
test_execution(code)

