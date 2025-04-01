import copy
import tokenize, io
from scipy import sparse


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            sa = sparse.random(10, 10, density=0.01, format="csr", random_state=42)
            sb = sparse.random(10, 10, density=0.01, format="csr", random_state=45)
        return sa, sb

    def generate_ans(data):
        _a = data
        sa, sb = _a
        result = sparse.hstack((sa, sb)).tocsr()
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert type(result) == sparse.csr.csr_matrix
    assert len(sparse.find(result != ans)[0]) == 0
    return 1


exec_context = r"""
from scipy import sparse
sa, sb = test_input
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
    assert (
        "toarray" not in tokens
        and "array" not in tokens
        and "todense" not in tokens
        and "A" not in tokens
    )

code = '\nimport scipy.sparse as sparse\nimport numpy as np\n\ndef hstack_csr(a, b):\n    if a.shape[0] != b.shape[0]:\n        raise ValueError("Matrices must have the same number of rows")\n\n    a_data = a.data\n    a_indices = a.indices\n    a_indptr = a.indptr\n\n    b_data = b.data\n    b_indices = b.indices\n    b_indptr = b.indptr\n\n    new_data = np.concatenate((a_data, b_data))\n    new_indices = np.concatenate((a_indices, b_indices))\n    new_indptr = np.concatenate((a_indptr[:-1], b_indptr[1:] + a.shape[1]))\n\n    return sparse.csr_matrix((new_data, new_indices, new_indptr), shape=(a.shape[0], a.shape[1] + b.shape[1]))\n\nresult = hstack_csr(sa, sb)\n'
test_execution(code)
test_string(code)
