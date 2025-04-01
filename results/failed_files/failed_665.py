import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from PIL import Image


def skip_plt_cmds(l):
    return all(
        p not in l for p in ["plt.show()", "plt.clf()", "plt.close()", "savefig"]
    )


def generate_test_case(test_case_id):
    x = np.random.random((10, 10))
    nrow = 2
    ncol = 2
    fig = plt.figure(figsize=(ncol + 1, nrow + 1))
    gs = gridspec.GridSpec(
        nrow,
        ncol,
        wspace=0.0,
        hspace=0.0,
        top=1.0 - 0.5 / (nrow + 1),
        bottom=0.5 / (nrow + 1),
        left=0.5 / (ncol + 1),
        right=1 - 0.5 / (ncol + 1),
    )
    for i in range(nrow):
        for j in range(ncol):
            ax = plt.subplot(gs[i, j])
            ax.imshow(x)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
    plt.savefig("ans.png", bbox_inches="tight")
    plt.close()
    return None, None


def exec_test(result, ans):
    code_img = np.array(Image.open("output.png"))
    oracle_img = np.array(Image.open("ans.png"))
    sample_image_stat = code_img.shape == oracle_img.shape and np.allclose(
        code_img, oracle_img
    )
    if not sample_image_stat:
        f = plt.gcf()
        assert len(f.axes) == 4
        for ax in f.axes:
            assert len(ax.images) == 1
            assert ax.get_subplotspec()._gridspec.hspace == 0.0
            assert ax.get_subplotspec()._gridspec.wspace == 0.0
    return 1


exec_context = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
x = np.random.random((10, 10))
from matplotlib import gridspec
nrow = 2
ncol = 2
fig = plt.figure(figsize=(ncol + 1, nrow + 1))
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

code = '\ngs = gridspec.GridSpec(nrow, ncol)\nfor row in range(nrow):\n    for col in range(ncol):\n        ax = fig.add_subplot(gs[row, col])\n        ax.imshow(x)\n        ax.set_xticks([])\n        ax.set_yticks([])\nplt.subplots_adjust(wspace=0, hspace=0)\nplt.show()\n'
test_execution(code)

