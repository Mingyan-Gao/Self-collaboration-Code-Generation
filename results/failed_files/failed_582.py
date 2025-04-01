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
    f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={"width_ratios": [3, 1]})
    a0.plot(x, y)
    a1.plot(y, x)
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
        width_ratios = f._gridspecs[0].get_width_ratios()
        all_axes = f.get_axes()
        assert len(all_axes) == 2
        assert width_ratios == [3, 1]
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

code = "\nfig, axes = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})\naxes[0].plot(x, y)\naxes[1].plot(x, y**2)\nplt.show()\n"
test_execution(code)

