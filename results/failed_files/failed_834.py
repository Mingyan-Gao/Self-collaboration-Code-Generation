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
                ("reduce_dim", PCA()),
                ("poly", PolynomialFeatures()),
                ("svm", SVC()),
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

code = "\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.svm import SVC\nfrom sklearn.decomposition import PCA\nfrom sklearn.preprocessing import PolynomialFeatures\n\n# Step 1: Create a basic Pipeline\nestimators = [('reduce_dim', PCA()), ('svm', SVC())]\nclf = Pipeline(estimators)\n\n# Step 2: Attempt to insert a step using named_steps()\noriginal_steps = clf.named_steps.copy()\n# Inserting into named_steps() does not modify the original pipeline\n# named_steps = clf.named_steps\n# named_steps['poly'] = PolynomialFeatures()\n# print(clf.named_steps)\n# print(original_steps)\n# print(clf.named_steps == original_steps)\n\n# Step 3: Create a new Pipeline object with insertion\nestimators_insert = [('reduce_dim', PCA()), ('poly', PolynomialFeatures()), ('svm', SVC())]\nclf_insert = Pipeline(estimators_insert)\n\n# Step 4: Create a new Pipeline object with deletion\nestimators_delete = [('svm', SVC())]\nclf_delete = Pipeline(estimators_delete)\n\n# Step 5: Example code for insertion and deletion (creating new Pipeline objects)\n# Insertion\nestimators_new = [('reduce_dim', PCA()), ('poly', PolynomialFeatures()), ('svm', SVC())]\nclf_new = Pipeline(estimators_new)\n\n# Deletion\nestimators_new_delete = [('reduce_dim', PCA())]\nclf_new_delete = Pipeline(estimators_new_delete)\n"
test_execution(code)

