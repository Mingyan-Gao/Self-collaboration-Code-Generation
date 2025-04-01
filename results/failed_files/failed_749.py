import numpy as np
import itertools
import copy
import scipy.spatial.distance


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            example_array = np.array(
                [
                    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 2, 0, 2, 2, 0, 6, 0, 3, 3, 3],
                    [0, 0, 0, 0, 2, 2, 0, 0, 0, 3, 3, 3],
                    [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
                    [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3],
                    [1, 1, 1, 0, 0, 0, 3, 3, 3, 0, 0, 3],
                    [1, 1, 1, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                    [1, 1, 1, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 1, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
                ]
            )
        return example_array

    def generate_ans(data):
        _a = data
        example_array = _a
        n = example_array.max() + 1
        indexes = []
        for k in range(1, n):
            tmp = np.nonzero(example_array == k)
            tmp = np.asarray(tmp).T
            indexes.append(tmp)
        result = np.zeros((n - 1, n - 1))
        for i, j in itertools.combinations(range(n - 1), 2):
            d2 = scipy.spatial.distance.cdist(
                indexes[i], indexes[j], metric="sqeuclidean"
            )
            result[i, j] = result[j, i] = d2.min() ** 0.5
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert np.allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
import scipy.spatial.distance
example_array = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\nunique_ids = np.unique(example_array)\nregion_coords = {}\nfor region_id in unique_ids:\n    region_coords[region_id] = np.where(example_array == region_id)\n\nresults = []\nfor i in range(len(unique_ids)):\n    for j in range(i + 1, len(unique_ids)):\n        id1 = unique_ids[i]\n        id2 = unique_ids[j]\n        \n        if id1 == 0 or id2 == 0:\n            min_dist = np.inf\n        else:\n            coords1 = np.array(list(zip(region_coords[id1][0], region_coords[id1][1])))\n            coords2 = np.array(list(zip(region_coords[id2][0], region_coords[id2][1])))\n            \n            if len(coords1) == 0 or len(coords2) == 0:\n                min_dist = np.inf\n            else:\n                distances = scipy.spatial.distance.cdist(coords1, coords2, 'euclidean')\n                min_dist = np.min(distances)\n        \n        results.append((id1, id2, min_dist))\nresult = results\n"
test_execution(code)

