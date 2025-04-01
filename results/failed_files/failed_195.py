import pandas as pd
import numpy as np
import copy
import tokenize, io


def generate_test_case(test_case_id):
    def generate_ans(data):
        df = data
        return (
            df.join(
                pd.DataFrame(
                    df.var2.str.split(",", expand=True)
                    .stack()
                    .reset_index(level=1, drop=True),
                    columns=["var2 "],
                )
            )
            .drop("var2", 1)
            .rename(columns=str.strip)
            .reset_index(drop=True)
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

code = '\nimport dask.dataframe as dd\nimport dask.multiprocessing\nimport pandas as pd\n\ndf = pd.DataFrame([["A", "Z,Y"], ["B", "X"], ["C", "W,U,V"]], index=[1,2,3], columns=[\'var1\', \'var2\'])\nddf = dd.from_pandas(df, npartitions=2)\n\ndef split_string(df):\n    df[\'var2\'] = df[\'var2\'].str.split(\',\')\n    return df\n\nddf = ddf.map_partitions(split_string, meta=ddf)\nlengths = ddf[\'var2\'].apply(len, meta=(\'var2\', \'int\')).compute()\n\nddf = ddf.explode(\'var2\')\n\nresult = ddf.repartition(npartitions=2)\n'
test_execution(code)
test_string(code)
