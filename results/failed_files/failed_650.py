import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import matplotlib


def skip_plt_cmds(l):
    return all(
        p not in l for p in ["plt.show()", "plt.clf()", "plt.close()", "savefig"]
    )


def generate_test_case(test_case_id):
    df = sns.load_dataset("penguins")[
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    ].head(10)
    bbox = [0, 0, 1, 1]
    plt.table(cellText=df.values, rowLabels=df.index, bbox=bbox, colLabels=df.columns)
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
        table_in_children = False
        for tab in ax.get_children():
            if isinstance(tab, matplotlib.table.Table):
                table_in_children = True
                break
        assert tuple(ax.get_children()[0]._bbox) == (0, 0, 1, 1)
    return 1


exec_context = r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = sns.load_dataset("penguins")[
    ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
].head(10)
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

code = "\nfig, ax = plt.subplots(figsize=(12, 4))\nax.axis('off')\ntable = plt.table(cellText=df.values, colLabels=df.columns, loc='center')\ntable.set_bbox([0, 0, 1, 1])\nplt.show()\n"
test_execution(code)

