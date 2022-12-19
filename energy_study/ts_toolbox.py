import pandas as pd
from scipy import stats


def descriptive_metrics(df, column_name):

    metrics = pd.DataFrame(
        data={
            "column": column_name,
            "count": df[column_name].count(),
            "median": df[column_name].median(),
            "mean": df[column_name].mean(),
            "std": df[column_name].std(),
            "variance": df[column_name].var(),
            "skewness": df[column_name].skew(),
            "kurtosis": df[column_name].kurt(),
        },
        index=[0],
    )

    return metrics


def normality(df, column_name):
    sw = stats.shapiro(df[column_name])
    ks_norm = stats.kstest(rvs=df[column_name], cdf="norm")

    ks_uniform = stats.kstest(rvs=df[column_name], cdf="uniform")

    error_metric = pd.DataFrame(
        data={
            "column": column_name,
            "count": len(df[column_name]),
            "shapiro-wilk statistic": sw.statistic,
            "shapiro-wilk p-value": sw.pvalue,
            "ks-n-test statistic": ks_norm.statistic,
            "ks-n-test p-value": ks_norm.pvalue,
            "ks-u-test statistic": ks_uniform.statistic,
            "ks-u-test p-value": ks_uniform.pvalue,
        },
        index=[0],
    )

    return error_metric
