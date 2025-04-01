import tensorflow as tf
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        FLAG = data
        return -805.02057

    def define_test_input(test_case_id):
        if test_case_id == 1:
            FLAG = 114514
        return FLAG

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        assert abs(result - ans) <= 0.02
        return 1
    except:
        return 0


exec_context = r"""
import tensorflow as tf
FLAG = test_input
[insert].numpy()
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\ntf.random.set_seed(10)\nA = tf.random.normal([100,100])\nB = tf.random.normal([100,100])\nresult = tf.reduce_sum(tf.matmul(A,B))\n'
test_execution(code)

