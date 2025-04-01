import numpy as np
import copy
from sklearn.cluster import KMeans
import sklearn
from sklearn.datasets import make_blobs


def generate_test_case(test_case_id):

    def define_test_input(test_case_id):
        if test_case_id == 1:
            X, y = make_blobs(n_samples=200, n_features=3, centers=8, random_state=42)
            p = 2
        elif test_case_id == 2:
            X, y = make_blobs(n_samples=200, n_features=3, centers=8, random_state=42)
            p = 3
        return p, X

    def generate_ans(data):
        p, X = data
        km = KMeans(n_clusters=8, random_state=42)
        km.fit(X)
        d = km.transform(X)[:, p]
        indexes = np.argsort(d)[::][:50]
        closest_50_samples = X[indexes]
        return closest_50_samples

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))

    return test_input, expected_result


def exec_test(result, ans):
    try:
        np.testing.assert_allclose(result, ans)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
p, X = test_input
km = KMeans(n_clusters=8, random_state=42)
def get_samples(p, X, km):
[insert]
closest_50_samples = get_samples(p, X, km)
result = closest_50_samples
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\n    center = km.cluster_centers_[p]\n    distances = np.linalg.norm(X - center, axis=1)\n    closest_indices = np.argsort(distances)[:50]\n    closest_samples = X[closest_indices]\n    return closest_samples\n### END SOLUTION\n'
test_execution(code)

