import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from PIL import Image


def skip_plt_cmds(l):
    return all(
        p not in l for p in ["plt.show()", "plt.clf()", "plt.close()", "savefig"]
    )


def generate_test_case(test_case_id):
    rc("mathtext", default="regular")
    time = np.arange(10)
    temp = np.random.random(10) * 30
    Swdown = np.random.random(10) * 100 - 10
    Rn = np.random.random(10) * 100 - 10
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(time, Swdown, "-", label="Swdown")
    ax.plot(time, Rn, "-", label="Rn")
    ax2 = ax.twinx()
    ax2.plot(time, temp, "-r", label="temp")
    ax.legend(loc=0)
    ax.grid()
    ax.set_xlabel("Time (h)")
    ax.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
    ax2.set_ylabel(r"Temperature ($^\circ$C)")
    ax2.set_ylim(0, 35)
    ax.set_ylim(-20, 100)
    plt.show()
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(time, Swdown, "-", label="Swdown")
    ax.plot(time, Rn, "-", label="Rn")
    ax2 = ax.twinx()
    ax2.plot(time, temp, "-r", label="temp")
    ax.legend(loc=0)
    ax.grid()
    ax.set_xlabel("Time (h)")
    ax.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
    ax2.set_ylabel(r"Temperature ($^\circ$C)")
    ax2.set_ylim(0, 35)
    ax.set_ylim(-20, 100)
    ax2.legend(loc=0)
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
        plt.show()
        assert len(f.axes) == 2
        assert len(f.axes[0].get_lines()) == 2
        assert len(f.axes[1].get_lines()) == 1
        assert len(f.axes[0]._twinned_axes.get_siblings(f.axes[0])) == 2
        if len(f.legends) == 1:
            assert len(f.legends[0].get_texts()) == 3
        elif len(f.legends) > 1:
            assert False
        else:
            assert len(f.axes[0].get_legend().get_texts()) == 2
            assert len(f.axes[1].get_legend().get_texts()) == 1
    return 1


exec_context = r"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc("mathtext", default="regular")
time = np.arange(10)
temp = np.random.random(10) * 30
Swdown = np.random.random(10) * 100 - 10
Rn = np.random.random(10) * 100 - 10
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time, Swdown, "-", label="Swdown")
ax.plot(time, Rn, "-", label="Rn")
ax2 = ax.twinx()
ax2.plot(time, temp, "-r", label="temp")
ax.legend(loc=0)
ax.grid()
ax.set_xlabel("Time (h)")
ax.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
ax2.set_ylabel(r"Temperature ($^\circ$C)")
ax2.set_ylim(0, 35)
ax.set_ylim(-20, 100)
plt.show()
plt.clf()
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

code = '\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom matplotlib import rc\n\nrc("mathtext", default="regular")\n\ntime = np.arange(10)\ntemp = np.random.random(10) * 30\nSwdown = np.random.random(10) * 100 - 10\nRn = np.random.random(10) * 100 - 10\n\nfig = plt.figure()\nax = fig.add_subplot(111)\nline1, = ax.plot(time, Swdown, "-", label="Swdown")\nline2, = ax.plot(time, Rn, "-", label="Rn")\nax2 = ax.twinx()\nline3, = ax2.plot(time, temp, "-r", label="temp")\n\nlines = [line1, line2, line3]\nlabels = [line.get_label() for line in lines]\nax.legend(lines, labels, loc=0)\n\nax.grid()\nax.set_xlabel("Time (h)")\nax.set_ylabel(r"Radiation ($MJ\\,m^{-2}\\,d^{-1}$)")\nax2.set_ylabel(r"Temperature ($^\\circ$C)")\nax2.set_ylim(0, 35)\nax.set_ylim(-20, 100)\nplt.show()\nplt.clf()\n'
test_execution(code)

