from datetime import datetime

import pandas as pd
import seaborn as sns
from energy_study.common import (
    BASE_DIR,
    DataColumnSpec,
)


def prepare_data(file_name):
    """
    "eCO2mix_RTE_Annuel-Definitif_2020.xls"
    """
    sns.set(rc={"figure.figsize": (14, 10)})

    df = pd.read_csv(BASE_DIR / file_name, delimiter="\t", index_col=False)

    df.rename(
        columns={"Prévision J-1": "Prévision_J_1", "Heures": "Hour"}, inplace=True
    )
    df = df[df[DataColumnSpec.CONSUMPTION].notna()]

    df["DateTime"] = [
        datetime.strptime(f"{date} {hour}", "%Y-%m-%d %H:%M")
        for date, hour in zip(df["Date"], df["Hour"])
    ]

    df = df.set_index("DateTime")

    df["Year"] = df.index.year
    df["Month"] = df.index.month_name()
    df["Day"] = df.index.day_name()

    df[DataColumnSpec.ENERGY_SOURCES] /= 1000
    df[[DataColumnSpec.CONSUMPTION, DataColumnSpec.FORECAST]] /= 1000

    df["FOSSIL_SUM"] = df[DataColumnSpec.FOSSIL_SOURCES].sum(axis=1)

    for calculated_field in DataColumnSpec.calculated_field_mappings():
        df[calculated_field] = df.eval(getattr(DataColumnSpec, calculated_field)())

    df.rename(columns=DataColumnSpec.mappings(), inplace=True)

    return df
