import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        time = df.time.tolist()
        car = df.car.tolist()
        farmost_neighbour = []
        euclidean_distance = []
        for i in range(len(df)):
            n = 0
            d = 0
            for j in range(len(df)):
                if (
                    df.loc[i, "time"] == df.loc[j, "time"]
                    and df.loc[i, "car"] != df.loc[j, "car"]
                ):
                    t = np.sqrt(
                        ((df.loc[i, "x"] - df.loc[j, "x"]) ** 2)
                        + ((df.loc[i, "y"] - df.loc[j, "y"]) ** 2)
                    )
                    if t >= d:
                        d = t
                        n = df.loc[j, "car"]
            farmost_neighbour.append(n)
            euclidean_distance.append(d)
        return pd.DataFrame(
            {
                "time": time,
                "car": car,
                "farmost_neighbour": farmost_neighbour,
                "euclidean_distance": euclidean_distance,
            }
        )

    def define_test_input(test_case_id):
        if test_case_id == 1:
            time = [0, 0, 0, 1, 1, 2, 2]
            x = [216, 218, 217, 280, 290, 130, 132]
            y = [13, 12, 12, 110, 109, 3, 56]
            car = [1, 2, 3, 1, 3, 4, 5]
            df = pd.DataFrame({"time": time, "x": x, "y": y, "car": car})
        if test_case_id == 2:
            time = [0, 0, 0, 1, 1, 2, 2]
            x = [219, 219, 216, 280, 290, 130, 132]
            y = [15, 11, 14, 110, 109, 3, 56]
            car = [1, 2, 3, 1, 3, 4, 5]
            df = pd.DataFrame({"time": time, "x": x, "y": y, "car": car})
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        result.euclidean_distance = np.round(result.euclidean_distance, 2)
        ans.euclidean_distance = np.round(ans.euclidean_distance, 2)
        pd.testing.assert_frame_equal(result, ans, check_dtype=False)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
df = test_input
[insert]
result = df
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\nfrom scipy.spatial.distance import cdist\nimport numpy as np\n\ndef calculate_distances(group):\n    points = group[['x', 'y']].to_numpy()\n    cars = group['car'].to_numpy()\n    distances = cdist(points, points, metric='euclidean')\n    \n    farthest_neighbors = []\n    euclidean_distances = []\n    \n    for i in range(len(cars)):\n        distances_i = distances[i]\n        distances_i[i] = -1  # Exclude self from being the farthest neighbor\n        farthest_neighbor_index = np.argmax(distances_i)\n        farthest_neighbor = cars[farthest_neighbor_index]\n        euclidean_distance = distances_i[farthest_neighbor_index]\n        \n        farthest_neighbors.append(farthest_neighbor)\n        euclidean_distances.append(euclidean_distance)\n    \n    group['farmost_neighbour'] = farthest_neighbors\n    group['euclidean_distance'] = euclidean_distances\n    return group[['car', 'farmost_neighbour', 'euclidean_distance']]\n\ndf2 = df.groupby('time').apply(calculate_distances).reset_index()\ndf = df2.groupby('time')['euclidean_distance'].mean()\n"
test_execution(code)

