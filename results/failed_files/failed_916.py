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

code = "\nimport numpy as np\nimport pandas as pd\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.preprocessing import LabelEncoder\n\nnew_X = [['asdf', '1'], ['asdf', '0'], ['qwer', '1']]\ny = ['2', '3', '4']\n\n# Convert to pandas DataFrame for easier encoding\ndf = pd.DataFrame(new_X)\n\n# Apply Label Encoding to each column\nfor col in df.columns:\n    le = LabelEncoder()\n    df[col] = le.fit_transform(df[col])\n\n# Convert back to numpy array\nnew_X_encoded = df.values\n\nclf = DecisionTreeClassifier()\nclf.fit(new_X_encoded, y)\n"
test_execution(code)

