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
    x = np.linspace(0, 2 * np.pi, 10)
    y = np.cos(x)
    plt.plot(x, y, label="sin")
    plt.xticks(rotation=-45)
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
        x = ax.get_xaxis()
        labels = ax.get_xticklabels()
        for l in labels:
            assert l.get_rotation() == 360 - 45
    return 1


exec_context = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
x = np.linspace(0, 2 * np.pi, 10)
y = np.cos(x)
plt.plot(x, y, label="sin")
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

code = '\nplt.xticks(rotation=45)\nplt.show()\n'
test_execution(code)

