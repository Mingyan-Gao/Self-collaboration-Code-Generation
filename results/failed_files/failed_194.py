import pandas as pd
import numpy as np
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return df.drop("var2", axis=1).join(
            df.var2.str.split(",", expand=True)
            .stack()
            .reset_index(drop=True, level=1)
            .rename("var2")
        )

    def define_test_input(test_case_id):
        if test_case_id == 1:
            df = pd.DataFrame(
                [["A", "Z,Y"], ["B", "X"], ["C", "W,U,V"]],
                index=[1, 2, 3],
                columns=["var1", "var2"],
            )
        if test_case_id == 2:
            df = pd.DataFrame(
                [["A", "Z,Y,X"], ["B", "W"], ["C", "U,V"]],
                index=[1, 2, 3],
                columns=["var1", "var2"],
            )
        return df

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        pd.testing.assert_frame_equal(result, ans, check_dtype=False)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
df = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)


def test_string(solution: str):
    tokens = []
    for token in tokenize.tokenize(io.BytesIO(solution.encode("utf-8")).readline):
        tokens.append(token.string)
    assert "for" not in tokens and "while" not in tokens

code = '\nimport dask.dataframe as dd\nimport pandas as pd\n\ndf = pd.DataFrame([["A", "Z,Y"], ["B", "X"], ["C", "W,U,V"]], index=[1,2,3], columns=[\'var1\', \'var2\'])\n\nddf = dd.from_pandas(df, npartitions=1)\n\ndef split_func(x):\n    if isinstance(x, str):\n        return x.split(\',\')\n    else:\n        return []\n\nddf[\'var2\'] = ddf[\'var2\'].map(split_func, meta=pd.Series(dtype=\'object\'))\n\ndef explode(df):\n    df = df.explode(\'var2\')\n    return df\n\nmeta = pd.DataFrame({\n    \'var1\': pd.Series(dtype=\'object\'),\n    \'var2\': pd.Series(dtype=\'object\')\n})\n\nresult = ddf.map_partitions(explode, meta=meta)\n'
test_execution(code)
test_string(code)
