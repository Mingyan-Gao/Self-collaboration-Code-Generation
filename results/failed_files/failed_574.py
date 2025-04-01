import matplotlib.pyplot as plt
import numpy
from PIL import Image
import numpy as np


def skip_plt_cmds(l):
    return all(
        p not in l for p in ["plt.show()", "plt.clf()", "plt.close()", "savefig"]
    )


def generate_test_case(test_case_id):
    xlabels = list("ABCD")
    ylabels = list("CDEF")
    rand_mat = numpy.random.rand(4, 4)
    plt.pcolor(rand_mat)
    plt.xticks(numpy.arange(0.5, len(xlabels)), xlabels)
    plt.yticks(numpy.arange(0.5, len(ylabels)), ylabels)
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    plt.savefig("ans.png", bbox_inches="tight")
    plt.close()
    return None, None


def exec_test(result, ans):
    xlabels = list("ABCD")
    ylabels = list("CDEF")
    code_img = np.array(Image.open("output.png"))
    oracle_img = np.array(Image.open("ans.png"))
    sample_image_stat = code_img.shape == oracle_img.shape and np.allclose(
        code_img, oracle_img
    )
    if not sample_image_stat:
        ax = plt.gca()
        assert ax.get_ylim()[0] > ax.get_ylim()[1]
        assert ax.xaxis._major_tick_kw["tick2On"]
        assert ax.xaxis._major_tick_kw["label2On"]
        assert not ax.xaxis._major_tick_kw["tick1On"]
        assert not ax.xaxis._major_tick_kw["label1On"]
        assert len(ax.get_xticklabels()) == len(xlabels)
        assert len(ax.get_yticklabels()) == len(ylabels)
    return 1


exec_context = r"""
import matplotlib.pyplot as plt
import numpy
xlabels = list("ABCD")
ylabels = list("CDEF")
rand_mat = numpy.random.rand(4, 4)
[insert]
plt.savefig('output.png', bbox_inches ='tight')
result = None
"""


def test_execution(solution: str):
    solution = "\n".join(filter(skip_plt_cmds, solution.split("\n")))
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\nplt.imshow(rand_mat)\nplt.xticks(numpy.arange(len(xlabels)), labels=xlabels, rotation=0)\nplt.yticks(numpy.arange(len(ylabels)), labels=ylabels)\nplt.gca().xaxis.tick_top()\nplt.gca().invert_yaxis()\nplt.show()\n'
test_execution(code)

