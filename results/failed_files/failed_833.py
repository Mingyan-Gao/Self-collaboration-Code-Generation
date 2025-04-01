import numpy as np
import copy
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVC
from sklearn.decomposition import PCA


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            estimators = [
                ("reduce_dIm", PCA()),
                ("pOly", PolynomialFeatures()),
                ("svdm", SVC()),
            ]
        elif test_case_id == 2:
            estimators = [
                ("reduce_poly", PolynomialFeatures()),
                ("dim_svm", PCA()),
                ("extra", PCA()),
                ("sVm_233", SVC()),
            ]
        return estimators

    def generate_ans(data):
        estimators = data
        clf = Pipeline(estimators)
        clf.steps.pop(1)
        names = str(clf.named_steps)
        return names

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        np.testing.assert_equal(result, ans)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.preprocessing import PolynomialFeatures
estimators = test_input
clf = Pipeline(estimators)
[insert]
result = str(clf.named_steps)
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nimport pandas as pd\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.svm import SVC\nfrom sklearn.decomposition import PCA\nfrom sklearn.preprocessing import PolynomialFeatures\nestimators = [(\'reduce_dim\', PCA()), (\'poly\', PolynomialFeatures()), (\'svm\', SVC())]\nclf = Pipeline(estimators)\n\nprint("Original Pipeline:")\nprint(clf)\nprint("Original named_steps:")\nprint(clf.named_steps)\n\ndel clf.named_steps[\'poly\']\n\nclf.steps = [(name, step) for name, step in clf.named_steps.items()]\n\nprint("\\nModified Pipeline:")\nprint(clf)\nprint("Modified named_steps:")\nprint(clf.named_steps)\n'
test_execution(code)

