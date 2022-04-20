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
