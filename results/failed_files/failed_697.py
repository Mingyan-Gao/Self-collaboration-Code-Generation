import tensorflow as tf
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def generate_ans(data):
        x = data
        return [tf.compat.as_str_any(a) for a in x]

    def define_test_input(test_case_id):
        if test_case_id == 1:
            x = [
                b"\xd8\xa8\xd9\x85\xd8\xb3\xd8\xa3\xd9\x84\xd8\xa9",
                b"\xd8\xa5\xd9\x86\xd8\xb4\xd8\xa7\xd8\xa1",
                b"\xd9\x82\xd8\xb6\xd8\xa7\xd8\xa1",
                b"\xd8\xac\xd9\x86\xd8\xa7\xd8\xa6\xd9\x8a",
                b"\xd8\xaf\xd9\x88\xd9\x84\xd9\x8a",
            ]
        return x

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        assert result == ans
        return 1
    except:
        return 0


exec_context = r"""
import tensorflow as tf
x = test_input
def f(x):
[insert]
result = f(x)
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
    assert "tf" in tokens

code = "\n    result = []\n    for byte_string in x:\n        decoded_unicode = tf.strings.unicode_decode(byte_string, 'UTF-8', errors='ignore')\n        decoded_string = decoded_unicode.numpy().decode('utf-8')\n        result.append(decoded_string)\n    return result\n"
test_execution(code)
test_string(code)
