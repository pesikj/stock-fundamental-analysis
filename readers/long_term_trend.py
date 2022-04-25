import os
import pandas
from readers import common


def read_data(stock_code="MSFT", value_name="ROA", filename="ROA.xlsx"):
    file_path = os.path.join("data", stock_code, filename)
    df = pandas.read_excel(file_path, skiprows=3)
    df = df.iloc[:-1]
    df = df.rename(columns={"Unnamed: 0": "Date"})
    df["Date"] = pandas.to_datetime(df["Date"])
    if value_name == "ROA":
        df = df[["Date", value_name, "Net income", "Total assets"]]
    elif value_name == "ROE":
        df = df[["Date", value_name, "Net income", "Stockholders’ equity"]]
    elif value_name == "OPM":
        df = df[["Date", value_name, "Operating income", "Revenue"]]
    df["DateNext"] = df["Date"] + pandas.Timedelta(days=1)
    df = df.sort_values(by=["Date"])
    return df


def read_market_data(filename="ROA.xlsx"):
    file_path = os.path.join("data", "Market", filename)
    df = pandas.read_excel(file_path, skiprows=3)
    df = df.iloc[:-1]
    df = df.rename(columns={"Unnamed: 0": "Date"})
    df = df.rename(columns=common.NAME_TO_TICK_DICT)
    df["Date"] = pandas.to_datetime(df["Date"])
    df = df.sort_values(by=["Date"])
    return df

