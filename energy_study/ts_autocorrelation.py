from rpy2.robjects import FloatVector, r
from rpy2.robjects.packages import importr
import statsmodels.api as sm
import numpy as np


class AutocorrelationTests:
    def __init__(self, lags) -> None:
        importr("TSA")
        self.lags = lags

    def ljung_box(self, x):
        """
        Ljung-Box Portmanteau test is a test for autocorrelation in either raw data or model residuals.
        """
        ljungbox_result = sm.stats.acorr_ljungbox(x, lags=self.lags, return_df=True)
        return ljungbox_result.to_markdown()

    def mcleod_li(self, x):
        """
        McLeod-Li Portmanteau test is a test for autoregressive conditional heteroskedasticity
        on raw data or residuals.
        The test checks for the presence of conditional heteroscedascity by
        computing the Ljung-Box (port-manteau) test with the squared data

        results:
            pvlaues the vector of p-values for the Ljung-Box
            test statistics computed using the first m lags of
            the ACF of the squared data or residuals, for m ranging from 1 to gof.lag.
        """
        x_for_r = FloatVector(x.ravel())  # converted R float vector
        mcleod_li_result = r["McLeod.Li.test"](
            y=x_for_r, plot=False, gof_lag=max(self.lags)
        )
        mcleod_li_result_list = list(
            dict(zip(mcleod_li_result.names, list(mcleod_li_result)))["p.values"]
        )
        pvalues_0s = sum(np.array(mcleod_li_result_list) == 0)
        return pvalues_0s, mcleod_li_result_list
