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
    x = np.arange(10)
    y = np.random.randn(10)
    plt.scatter(x, y)
    ax = plt.gca()
    ax.xaxis.set_ticks([3, 4])
    ax.xaxis.grid(True)
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
        np.testing.assert_equal([3, 4], ax.get_xticks())
        xlines = ax.get_xaxis()
        l = xlines.get_gridlines()[0]
        assert l.get_visible()
        ylines = ax.get_yaxis()
        l = ylines.get_gridlines()[0]
        assert not l.get_visible()
    return 1


exec_context = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
x = np.arange(10)
y = np.random.randn(10)
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

code = "\nxticks = plt.xticks()[0]\nnew_xticks = np.unique(np.append(xticks, [3, 4]))\nplt.xticks(new_xticks)\nplt.grid(axis='x')\nplt.axvline(x=3, color='gray', linestyle='--')\nplt.axvline(x=4, color='gray', linestyle='--')\n"
test_execution(code)

