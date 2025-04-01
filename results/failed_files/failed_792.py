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
        result = sparse.vstack((sa, sb)).tocsr()
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

code = '\nimport numpy as np\nsa_data = sa.data\nsa_indices = sa.indices\nsa_indptr = sa.indptr\nsb_data = sb.data\nsb_indices = sb.indices\nsb_indptr = sb.indptr\ndata = np.concatenate((sa_data, sb_data))\nindices = np.concatenate((sa_indices, sb_indices))\nindptr = np.concatenate((sa_indptr[:-1], sb_indptr[1:] + sa_indptr[-1]))\nresult = sparse.csr_matrix((data, indices, indptr), shape=(sa.shape[0] + sb.shape[0], sa.shape[1]))\n'
test_execution(code)
test_string(code)
