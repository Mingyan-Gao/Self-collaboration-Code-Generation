import numpy as np
import pandas as pd
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            probabilit = [0.333, 0.334, 0.333]
            lista_elegir = [(3, 3), (3, 4), (3, 5)]
            samples = 1000
        elif test_case_id == 2:
            np.random.seed(42)
            probabilit = np.zeros(10)
            probabilit[np.random.randint(0, 10)] = 1
            lista_elegir = [
                (x, y) for x, y in zip(np.arange(0, 10), np.arange(10, 0, -1))
            ]
            samples = 10
        return probabilit, lista_elegir, samples

    def generate_ans(data):
        _a = data
        probabilit, lista_elegir, samples = _a
        np.random.seed(42)
        temp = np.array(lista_elegir)
        result = temp[np.random.choice(len(lista_elegir), samples, p=probabilit)]
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    tuples = np.unique(ans, axis=0)
    for tuple in tuples:
        ratio = np.sum(np.all(result == tuple, axis=-1)) / result.shape[0]
        ans_ratio = np.sum(np.all(ans == tuple, axis=-1)) / ans.shape[0]
        assert abs(ratio - ans_ratio) <= 0.05
    return 1


exec_context = r"""
import numpy as np
probabilit, lista_elegir, samples = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)


def test_string(solution: str):
    tokens = []
    for token in tokenize.tokenize(io.BytesIO(solution.encode("utf-8")).readline):
        tokens.append(token.string)
    assert "choice" in tokens

code = '\nimport numpy as np\n\nprobabilit = [0.333, 0.334, 0.333]\nlista_elegir = [(3, 3), (3, 4), (3, 5)]\nsamples = 1000\n\nprobabilit = np.array(probabilit)\nprobabilit /= probabilit.sum()\nresult = np.random.choice(lista_elegir, samples, p=probabilit)\n'
test_execution(code)
test_string(code)
