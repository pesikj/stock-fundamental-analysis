import os
import pandas
from readers import common

from readers import prices


def read_market_data(files_to_process=()):
    df_merged = None
    for item in files_to_process:
        file_path = os.path.join("data", "Market", item[0])
        df = pandas.read_excel(file_path, skiprows=3)
        df = df.rename(columns={"Unnamed: 0": "Company"})
        df["Company"] = df["Company"].str.replace(item[1], "Microsoft Corp.")
        df = df[df["Company"].isin(common.NAME_TO_TICK_DICT.keys())]
        for key, value in common.NAME_TO_TICK_DICT.items():
            df["Company"] = df["Company"].str.replace(key, value)
        df = pandas.melt(df, id_vars="Company", value_vars=df.columns[1:], value_name=item[1], var_name="Date")
        if df_merged is None:
            df_merged = df
        else:
            df_merged = pandas.merge(df_merged, df, on=["Company", "Date"], how="left")
    df_prices_all = prices.read_all_data()
    df_merged = df_merged.sort_values(["Date"])
    df_merged = pandas.merge_asof(df_merged, df_prices_all[["DateNext", "Adj_Close", "Company"]], left_on="Date",
                                right_on="DateNext", by="Company", direction='forward')
    df_merged = df_merged.drop(labels="DateNext", axis=1)
    return df_merged

