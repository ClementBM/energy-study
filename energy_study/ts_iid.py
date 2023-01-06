from rpy2.robjects import FloatVector, r
from rpy2.robjects.packages import importr
import pandas as pd


class IidTests:
    def __init__(self) -> None:
        importr("spgs")

    def turning_point(self, x):
        """
        Turning point test

        Perform a test of statistical independence of a data series by comparing
        the number of turning points present in the series with the number of turning
        points expected to be present in an i.i.d. series.
        This test is useful for detecting cyclic/periodic trends in data series.

        H0: the data series is i.i.d. (not trending)
        H1: the data series is not i.i.d. (trending)

        Results:
            statistic : the value of the test statistic.
            p.value : the p-value of the test.
            method : a character string indicating what type of test was performed.
            data.name : a character string giving the name of the data.
            n : the number of points in the data series.
            mu : The expected number of turning points that would be seen in an i.i.d. series.
            sigma : The standard deviation of the number of turning points that would be seen in an i.i.d. series.
        """
        x_for_r = FloatVector(x.ravel())
        result = r["turningpoint.test"](x_for_r)
        result_dict = {
            key: list(value.items())[-1][-1]
            for key, value in result.items()
            if key in ["statistic", "p.value", "n", "mu", "sigma"]
        }
        return pd.DataFrame(result_dict, index=[0])

    def rank(self, x):
        """
        Rank test

        Test for a trend in a data series by comparing the number of increasing
        pairs in the series with the number expected in an i.i.d. series.
        This test is useful for detecting linear trends in data series.

        H0: the data series is i.i.d. (not trending)
        H1: the data series is not i.i.d. (trending)

        Results:
            statistic : the value of the test statistic.
            p.value : the p-value of the test.
            method : a character string indicating what type of test was performed.
            data.name : a character string giving the name of the data.
            pairs : the number of increasing pairs counted in the data series.
            n : the number of points in the data series.
            mu : The expected number of increasing pairs that would be seen in an i.i.d. series.
            sigma : The standard deviation of the number of increasing pairs that would be seen in an i.i.d. series
        """
        x_for_r = FloatVector(x.ravel())
        result = r["rank.test"](x_for_r)
        result_dict = {
            key: list(value.items())[-1][-1]
            for key, value in result.items()
            if key in ["statistic", "p.value", "pairs", "n", "mu", "sigma"]
        }
        return pd.DataFrame(result_dict, index=[0])
