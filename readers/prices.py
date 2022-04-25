import os
import pandas


def read_data(stock_code="MSFT"):
    file_path = os.path.join("data", stock_code, "prices.csv")
    df = pandas.read_csv(file_path)
    df["Date"] = pandas.to_datetime(df["Date"])
    df = df.rename(columns={"Adj Close": "Adj_Close"})
    df = df.sort_values(by=["Date"])
    df["DateNext"] = df["Date"] + pandas.Timedelta(days=1)
    return df

def read_all_data():
    df_all = None
    for item in os.listdir("data"):
        stock_code = item
        file_path = os.path.join("data", stock_code, "prices.csv")
        if item == "Market":
            continue
        df = pandas.read_csv(file_path)
        df["Date"] = pandas.to_datetime(df["Date"])
        df = df.rename(columns={"Adj Close": "Adj_Close"})
        df = df.sort_values(by=["Date"])
        df["DateNext"] = df["Date"] + pandas.Timedelta(days=-1)
        df["Company"] = item
        if df_all is None:
            df_all = df
        else:
            df_all = pandas.concat([df_all, df])
    df_all = df_all.sort_values(["DateNext"])
    return df_all
