import numpy as np
import copy


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            A = np.asarray([[1, 1, 1], [1, 1, 2], [1, 1, 3], [1, 1, 4]])
            B = np.asarray(
                [
                    [0, 0, 0],
                    [1, 0, 2],
                    [1, 0, 3],
                    [1, 0, 4],
                    [1, 1, 0],
                    [1, 1, 1],
                    [1, 1, 4],
                ]
            )
        elif test_case_id == 2:
            np.random.seed(42)
            A = np.random.randint(0, 2, (10, 3))
            B = np.random.randint(0, 2, (20, 3))
        elif test_case_id == 3:
            A = np.asarray([[1, 1, 1], [1, 1, 4]])
            B = np.asarray(
                [
                    [0, 0, 0],
                    [1, 0, 2],
                    [1, 0, 3],
                    [1, 0, 4],
                    [1, 1, 0],
                    [1, 1, 1],
                    [1, 1, 4],
                ]
            )
        return A, B

    def generate_ans(data):
        _a = data
        A, B = _a
        dims = np.maximum(B.max(0), A.max(0)) + 1
        output = A[
            ~np.in1d(np.ravel_multi_index(A.T, dims), np.ravel_multi_index(B.T, dims))
        ]
        return output

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    if ans.shape[0]:
        np.testing.assert_array_equal(result, ans)
    else:
        result = result.reshape(0)
        ans = ans.reshape(0)
        np.testing.assert_array_equal(result, ans)
    return 1


exec_context = r"""
import numpy as np
A, B = test_input
[insert]
result = output
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(3):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nimport numpy as np\nA=np.asarray([[1,1,1], [1,1,2], [1,1,3], [1,1,4]])\nB=np.asarray([[0,0,0], [1,0,2], [1,0,3], [1,0,4], [1,1,0], [1,1,1], [1,1,4]])\n\nB_set = set(map(tuple, B))\nresult = []\nfor row in A:\n    if tuple(row) not in B_set:\n        result.append(row)\noutput = np.asarray(result)\n'
test_execution(code)

