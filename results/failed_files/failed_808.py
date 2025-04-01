import numpy as np
import copy
from scipy import integrate, stats


def generate_test_case(test_case_id):
    def define_test_input(test_case_id):
        if test_case_id == 1:
            range_start = 1
            range_end = 10
            estimated_a, estimated_m, estimated_d = 1, 1, 1
            sample_data = [1.5, 1.6, 1.8, 2.1, 2.2, 3.3, 4, 6, 8, 9]
        return (
            range_start,
            range_end,
            estimated_a,
            estimated_m,
            estimated_d,
            sample_data,
        )

    def generate_ans(data):
        _a = data

        def bekkers(x, a, m, d):
            p = a * np.exp((-1 * (x ** (1 / 3) - m) ** 2) / (2 * d**2)) * x ** (-2 / 3)
            return p

        range_start, range_end, estimated_a, estimated_m, estimated_d, sample_data = _a

        def bekkers_cdf(x, a, m, d, range_start, range_end):
            values = []
            for value in x:
                integral = integrate.quad(
                    lambda k: bekkers(k, a, m, d), range_start, value
                )[0]
                normalized = (
                    integral
                    / integrate.quad(
                        lambda k: bekkers(k, a, m, d), range_start, range_end
                    )[0]
                )
                values.append(normalized)
            return np.array(values)

        result = stats.kstest(
            sample_data,
            lambda x: bekkers_cdf(
                x, estimated_a, estimated_m, estimated_d, range_start, range_end
            ),
        )
        return result

    test_input = define_test_input(test_case_id)
    expected_result = generate_ans(copy.deepcopy(test_input))
    return test_input, expected_result


def exec_test(result, ans):
    assert np.allclose(result, ans)
    return 1


exec_context = r"""
import numpy as np
import scipy as sp
from scipy import integrate,stats
def bekkers(x, a, m, d):
    p = a*np.exp((-1*(x**(1/3) - m)**2)/(2*d**2))*x**(-2/3)
    return(p)
range_start, range_end, estimated_a, estimated_m, estimated_d, sample_data = test_input
[insert]
"""


def test_execution(solution: str):
    code = exec_context.replace("[insert]", solution)
    for i in range(1):
        test_input, expected_result = generate_test_case(i + 1)
        test_env = {"test_input": test_input}
        exec(code, test_env)
        assert exec_test(test_env["result"], expected_result)

code = '\ndef cdf(x, a, m, d):\n    return integrate.quad(bekkers, range_start, x, args=(a, m, d))[0]\ncdf_func = lambda x: cdf(x, estimated_a, estimated_m, estimated_d)\nresult = stats.kstest(sample_data, cdf_func)\n'
test_execution(code)

