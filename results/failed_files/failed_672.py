import tensorflow as tf
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        labels = data
        t = tf.one_hot(indices=labels, depth=10, on_value=0, off_value=1, axis=-1)
        n = t.numpy()
        for i in range(len(n)):
            n[i] = n[i][::-1]
        return tf.constant(n)

    def define_test_input(test_case_id):
        if test_case_id == 1:
            labels = [0, 6, 5, 4, 2]
        if test_case_id == 2:
            labels = [0, 1, 2, 3, 4]
        return labels

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
        assert result.dtype == tf.int32
        return 1
    except:
        return 0


exec_context = r"""
import tensorflow as tf
labels = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nnum_classes = 10\nlabels_tensor = tf.constant(labels, dtype=tf.int32)\nresult = tf.ones((tf.shape(labels_tensor)[0], num_classes), dtype=tf.int32)\nindices = tf.stack([tf.range(tf.shape(labels_tensor)[0]), labels_tensor], axis=1)\nresult = tf.tensor_scatter_nd_update(result, indices, tf.zeros(tf.shape(labels_tensor), dtype=tf.int32))\n'
test_execution(code)

