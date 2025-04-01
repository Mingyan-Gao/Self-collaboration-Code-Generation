import tensorflow as tf
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        data = data
        a, b = data
        tile_a = tf.tile(tf.expand_dims(a, 1), [1, tf.shape(b)[0]])
        tile_a = tf.expand_dims(tile_a, 2)
        tile_b = tf.tile(tf.expand_dims(b, 0), [tf.shape(a)[0], 1])
        tile_b = tf.expand_dims(tile_b, 2)
        cart = tf.concat([tile_a, tile_b], axis=2)
        return cart

    def define_test_input(test_case_id):
        if test_case_id == 1:
            a = tf.constant([1, 2, 3])
            b = tf.constant([4, 5, 6, 7])
        return a, b

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    def tensor_equal(a, b):
        if type(a) != type(b):
            return False
        if isinstance(a, type(tf.constant([]))) is not True:
            if isinstance(a, type(tf.Variable([]))) is not True:
                return False
        if a.shape != b.shape:
            return False
        if a.dtype != tf.float32:
            a = tf.cast(a, tf.float32)
        if b.dtype != tf.float32:
            b = tf.cast(b, tf.float32)
        if not tf.reduce_min(tf.cast(a == b, dtype=tf.int32)):
            return False
        return True

    try:
        assert tensor_equal(result, ans)
        return 1
    except:
        return 0


exec_context = r"""
import tensorflow as tf
a,b = test_input
[insert]
if result.shape == [12,2]:
    result = tf.reshape(result, [3,4,2])
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\na_grid, b_grid = tf.meshgrid(a, b)\nstacked = tf.stack([a_grid, b_grid], axis=-1)\nresult = tf.reshape(stacked, [tf.size(a) * tf.size(b), 2])\n'
test_execution(code)

