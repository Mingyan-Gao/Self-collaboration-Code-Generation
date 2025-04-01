import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image


def skip_plt_cmds(l):
    return all(
        p not in l for p in ["plt.show()", "plt.clf()", "plt.close()", "savefig"]
    )


def generate_test_case(test_case_id):
    x = np.random.rand(10)
    y = np.random.rand(10)
    plt.scatter(x, y)
    plt.minorticks_on()
    ax = plt.gca()
    ax.tick_params(axis="x", which="minor", bottom=False)
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
        ax = plt.gca()
        assert len(ax.collections) == 1
        xticks = ax.xaxis.get_minor_ticks()
        for t in xticks:
            assert not t.tick1line.get_visible()
        yticks = ax.yaxis.get_minor_ticks()
        assert len(yticks) > 0
        for t in yticks:
            assert t.tick1line.get_visible()
    return 1


exec_context = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
x = np.random.rand(10)
y = np.random.rand(10)
plt.scatter(x, y)
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

code = "\nplt.minorticks_on()\nplt.tick_params(axis='y', which='minor')\nplt.show()\n"
test_execution(code)

