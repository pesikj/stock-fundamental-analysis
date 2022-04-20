import os
import pandas
from readers import common


def read_data(stock_code="MSFT"):
    file_path = os.path.join("data", stock_code, "ROA.xlsx")
    df = pandas.read_excel(file_path, skiprows=3)
    df = df.iloc[:-1]
    df = df.rename(columns={"Unnamed: 0": "Date"})
    df["Date"] = pandas.to_datetime(df["Date"])
    df = df[["Date", "ROA", "Net income", "Total assets"]]
    df["DateNext"] = df["Date"] + pandas.Timedelta(days=1)
    df = df.sort_values(by=["Date"])
    return df


def read_market_data():
    file_path = os.path.join("data", "Market", "ROA.xlsx")
    df = pandas.read_excel(file_path, skiprows=3)
    df = df.iloc[:-1]
    df = df.rename(columns={"Unnamed: 0": "Date"})
    df = df.rename(columns=common.NAME_TO_TICK_DICT)
    df["Date"] = pandas.to_datetime(df["Date"])
    df = df.sort_values(by=["Date"])
    return df

