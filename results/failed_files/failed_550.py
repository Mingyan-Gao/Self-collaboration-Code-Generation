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
    x = np.linspace(0, 2 * np.pi, 400)
    y1 = np.sin(x)
    y2 = np.cos(x)
    fig, (ax1, ax2) = plt.subplots(nrows=2, subplot_kw=dict(frameon=False))
    plt.subplots_adjust(hspace=0.0)
    ax1.grid()
    ax2.grid()
    ax1.plot(x, y1, color="r")
    ax2.plot(x, y2, color="b", linestyle="--")
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
        fig = plt.gcf()
        ax12 = fig.axes
        assert len(ax12) == 2
        ax1, ax2 = ax12
        assert not ax1.get_frame_on()
        assert not ax2.get_frame_on()
    return 1


exec_context = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
x = np.linspace(0, 2 * np.pi, 400)
y1 = np.sin(x)
y2 = np.cos(x)
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

code = "\nfig, (ax1, ax2) = plt.subplots(1, 2)\nax1.plot(x, y1)\nax2.plot(x, y2)\n\nax1.spines[['top', 'bottom', 'left', 'right']].set_visible(False)\nax2.spines[['top', 'bottom', 'left', 'right']].set_visible(False)\n\nplt.show()\n"
test_execution(code)

