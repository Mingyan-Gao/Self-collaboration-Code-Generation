import pandas as pd
import numpy as np
import copy


def generate_test_case(test_case_id):
    def generate_ans(data):
        s = data
        return pd.to_numeric(s.str.replace(",", ""), errors="coerce")

    def define_test_input(test_case_id):
        if test_case_id == 1:
            s = pd.Series(
                [
                    "2,144.78",
                    "2,036.62",
                    "1,916.60",
                    "1,809.40",
                    "1,711.97",
                    "6,667.22",
                    "5,373.59",
                    "4,071.00",
                    "3,050.20",
                    "-0.06",
                    "-1.88",
                    "",
                    "-0.13",
                    "",
                    "-0.14",
                    "0.07",
                    "0",
                    "0",
                ],
                index=[
                    "2016-10-31",
                    "2016-07-31",
                    "2016-04-30",
                    "2016-01-31",
                    "2015-10-31",
                    "2016-01-31",
                    "2015-01-31",
                    "2014-01-31",
                    "2013-01-31",
                    "2016-09-30",
                    "2016-06-30",
                    "2016-03-31",
                    "2015-12-31",
                    "2015-09-30",
                    "2015-12-31",
                    "2014-12-31",
                    "2013-12-31",
                    "2012-12-31",
                ],
            )
        if test_case_id == 2:
            s = pd.Series(
                [
                    "2,144.78",
                    "2,036.62",
                    "1,916.60",
                    "1,809.40",
                    "1,711.97",
                    "6,667.22",
                    "5,373.59",
                    "4,071.00",
                    "3,050.20",
                    "-0.06",
                    "-1.88",
                    "",
                    "-0.13",
                    "",
                    "-0.14",
                    "0.07",
                    "0",
                    "0",
                ],
                index=[
                    "2026-10-31",
                    "2026-07-31",
                    "2026-04-30",
                    "2026-01-31",
                    "2025-10-31",
                    "2026-01-31",
                    "2025-01-31",
                    "2024-01-31",
                    "2023-01-31",
                    "2026-09-30",
                    "2026-06-30",
                    "2026-03-31",
                    "2025-12-31",
                    "2025-09-30",
                    "2025-12-31",
                    "2024-12-31",
                    "2023-12-31",
                    "2022-12-31",
                ],
            )
        return s

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    try:
        pd.testing.assert_series_equal(result, ans, check_dtype=False)
        return 1
    except:
        return 0


exec_context = r"""
import pandas as pd
import numpy as np
s = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(2):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = "\ndef clean_and_convert(series):\n    series = series.fillna('')\n    series = series.astype(str)\n    series = series.str.replace(',', '')\n    return pd.to_numeric(series, errors='coerce')\n\ndf = pd.DataFrame({\n    'Revenue': ['24.73', '18.73', '17.56', '29.14', '22.67', '95.85', '84.58', '58.33', '29.63', '243.91', '230.77', '216.58', '206.23', '192.82', '741.15', '556.28', '414.51', '308.82', '2,144.78', '2,036.62', '1,916.60', '1,809.40', '1,711.97', '6,667.22', '5,373.59', '4,071.00', '3,050.20', '-0.06', '-1.88', '', '-0.13', '', '-0.14', '0.07', '0', '0', '-0.8', '-1.12', '1.32', '-0.05', '-0.34', '-1.37', '-1.9', '-1.48', '0.1', '41.98', '35', '-11.66', '27.09', '-3.44', '14.13', '-18.69', '-4.87', '-5.7'],\n    'Other, Net': ['-0.06', '-1.88', '', '-0.13', '', '-0.14', '0.07', '0', '0', '-0.8', '-1.12', '1.32', '-0.05', '-0.34', '-1.37', '-1.9', '-1.48', '0.1', '41.98', '35', '-11.66', '27.09', '-3.44', '14.13', '-18.69', '-4.87', '-5.7', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]\n})\n\ndf['Revenue'] = clean_and_convert(df['Revenue'])\ndf['Other, Net'] = clean_and_convert(df['Other, Net'])\n\nresult = df\n"
test_execution(code)

