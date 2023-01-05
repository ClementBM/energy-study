from statsmodels.tsa.stattools import adfuller, kpss
import pandas as pd


class StationarityTests:
    def __init__(self, max_lag=None, significance=0.05):
        self.significance_level = significance
        self.is_stationary = None
        self.max_lag = max_lag

    def adf(self, timeseries, diff=0, printResults=True):
        ts = timeseries.copy()
        if diff > 0:
            for _ in range(diff):
                ts = ts.diff()

        ts = ts.dropna()

        # Dickey-Fuller test
        if self.max_lag:
            adf_test = adfuller(ts, maxlag=self.max_lag, autolag=None)
        else:
            adf_test = adfuller(ts, autolag="AIC")
        p_value = adf_test[1]

        if p_value < self.significance_level:
            is_stationary = True
        else:
            is_stationary = False

        if printResults:
            df_results = pd.Series(
                adf_test[0:4],
                index=[
                    "ADF Test Statistic",
                    "p-Value",
                    "# Lags Used",
                    "# Observations Used",
                ],
            )

            # Add Critical Values
            for key, value in adf_test[4].items():
                df_results["Critical Value (%s)" % key] = value

            print("Augmented Dickey-Fuller Test Results:")
            print(df_results)

        return p_value, is_stationary

    def kpss(self, timeseries, diff=0, printResults=True):
        ts = timeseries.copy()

        if diff > 0:
            for _ in range(diff):
                ts = ts.diff()

        ts = ts.dropna()

        if self.max_lag:
            kpss_test = kpss(ts, regression="c", nlags=self.max_lag)
        else:
            kpss_test = kpss(ts, regression="c")

        p_value = kpss_test[1]

        if p_value > self.significance_level:
            is_stationary = True
        else:
            is_stationary = False

        if printResults:
            df_results = pd.Series(
                kpss_test[0:3],
                index=[
                    "KPSS test Statistic",
                    "p-Value",
                    "# Lags Used",
                ],
            )

            # Add Critical Values
            for key, value in kpss_test[3].items():
                df_results["Critical Value (%s)" % key] = value

            print("KPSS Test Results:")
            print(df_results)

        return p_value, is_stationary

    def until_stationarity(self, timeseries):
        is_stationary = False
        diff_count = 0
        kpss = []
        adf = []
        while not is_stationary:
            kpss_p_value, is_kpss_stationary = self.kpss(
                timeseries, diff=diff_count, printResults=False
            )
            adf_p_value, is_adf_stationary = self.adf(
                timeseries, diff=diff_count, printResults=False
            )

            is_stationary = is_kpss_stationary and is_adf_stationary

            kpss.append(kpss_p_value)
            adf.append(adf_p_value)

            diff_count += 1

        return pd.DataFrame(
            {
                "diff": range(diff_count),
                "adf": adf,
                "kpss": kpss,
            }
        )
