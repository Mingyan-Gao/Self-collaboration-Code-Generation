import seaborn as sns
import matplotlib.pylab as plt
import pandas
import numpy as np
from PIL import Image


def skip_plt_cmds(l):
    return all(
        p not in l for p in ["plt.show()", "plt.clf()", "plt.close()", "savefig"]
    )


def generate_test_case(test_case_id):
    df = pandas.DataFrame(
        {
            "a": np.arange(1, 31),
            "b": [
                "A",
            ]
            * 10
            + [
                "B",
            ]
            * 10
            + [
                "C",
            ]
            * 10,
            "c": np.random.rand(30),
        }
    )
    g = sns.FacetGrid(df, row="b")
    g.map(sns.pointplot, "a", "c")
    for ax in g.axes.flat:
        labels = ax.get_xticklabels()  # get x labels
        for i, l in enumerate(labels):
            if i % 2 == 0:
                labels[i] = ""  # skip even labels
        ax.set_xticklabels(labels)  # set new labels
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
        assert len(f.axes) == 3
        xticks = f.axes[-1].get_xticks()
        xticks = np.array(xticks)
        diff = xticks[1:] - xticks[:-1]
        assert np.all(diff == 1)
        xticklabels = []
        for label in f.axes[-1].get_xticklabels():
            if label.get_text() != "":
                xticklabels.append(int(label.get_text()))
        xticklabels = np.array(xticklabels)
        diff = xticklabels[1:] - xticklabels[:-1]
        assert np.all(diff == 2)
    return 1


exec_context = r"""
import seaborn as sns
import matplotlib.pylab as plt
import pandas
import numpy as np
df = pandas.DataFrame(
    {
        "a": np.arange(1, 31),
        "b": ["A",] * 10 + ["B",] * 10 + ["C",] * 10,
        "c": np.random.rand(30),
    }
)
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

code = '\ng = sns.FacetGrid(df, row="b")\ng.map(sns.pointplot, "a", "c")\nfor ax in g.axes.flat:\n    ax.set_xticks(np.arange(1, 31, 1))\n    ax.set_xticklabels(np.arange(1, 31, 2))\n'
test_execution(code)

