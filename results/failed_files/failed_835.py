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
                ("reduce_poly", PolynomialFeatures()),
                ("dim_svm", PCA()),
                ("sVm_233", SVC()),
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
        clf.steps.insert(0, ("reduce_dim", PCA()))
        length = len(clf.steps)
        return length

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
result = len(clf.steps)
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nimport pandas as pd\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.svm import SVC\nfrom sklearn.decomposition import PCA\nfrom sklearn.preprocessing import PolynomialFeatures\nfrom sklearn.linear_model import LogisticRegression\n\n# Create a Pipeline object \'clf\' with initial steps\nestimators = [(\'reduce_poly\', PolynomialFeatures()), (\'dim_svm\', PCA()), (\'sVm_233\', SVC())]\nclf = Pipeline(estimators)\n\n# Access the steps of the pipeline\nprint("Original Pipeline:")\nprint(clf.steps)\n\n# Inserting a new step into the pipeline\nnew_step = (\'logistic\', LogisticRegression())\nnew_steps = list(clf.steps)  # Convert to list for modification\nnew_steps.insert(1, new_step)  # Insert at index 1\nclf.steps = new_steps  # Assign the new list to clf.steps\n\nprint("\\nPipeline after inserting a step:")\nprint(clf.steps)\n\n# Deleting a step from the pipeline\ndel_index = 2  # Index of the step to delete\ndel new_steps[del_index]\nclf.steps = new_steps\n\nprint("\\nPipeline after deleting a step:")\nprint(clf.steps)\n'
test_execution(code)

