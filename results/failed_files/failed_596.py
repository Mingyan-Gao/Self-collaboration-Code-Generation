import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


def skip_plt_cmds(l):
    return all(
        p not in l for p in ["plt.show()", "plt.clf()", "plt.close()", "savefig"]
    )


def generate_test_case(test_case_id):
    x = np.arange(10)
    y = np.arange(10)
    (l,) = plt.plot(x, y, "o-", lw=10, markersize=30)
    l.set_markerfacecolor((1, 1, 0, 0.5))
    l.set_color("blue")
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
        lines = ax.get_lines()
        assert len(lines) == 1
        assert lines[0].get_markerfacecolor()
        assert not isinstance(lines[0].get_markerfacecolor(), str)
        assert lines[0].get_markerfacecolor()[-1] == 0.5
        assert isinstance(lines[0].get_color(), str) or lines[0].get_color()[-1] == 1
    return 1


exec_context = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
x = np.arange(10)
y = np.arange(10)
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

code = "\nplt.plot(x, y, marker='o', alpha=0.5)\nplt.show()\n"
test_execution(code)

