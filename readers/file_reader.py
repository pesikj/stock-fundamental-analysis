import os
import pandas
from readers import common


def find_row(df, indicator, row_name):
    for i in range(1, 15):
        test_value = df.iloc[i, 0]
        if test_value == row_name:
            df = df.iloc[[0, i]]
            df = df.rename({i: indicator})
            break
    return df


def read_file(company, file_name):
    file_path = os.path.join("data", company, file_name)
    if file_name == "Current-Ratio.xlsx":
        indicator = "CR"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="B:F")
        df = df.iloc[[0, 5]]
        df = df.rename({5: indicator})
        df = df.T
    elif file_name == "Debt-to-Assets.xlsx":
        indicator = "DA"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "Debt to assets")
        df = df.T
    elif file_name == "Financial-Leverage.xlsx":
        indicator = "FL"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "Financial leverage")
        df = df.T
    elif file_name == "Operating-Profit-Margin.xlsx":
        indicator = "OPM"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "Operating profit margin")
        df = df.T
    elif file_name == "Receivables-Turnover.xlsx":
        indicator = "RT"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "Receivables turnover")
        df = df.T
    elif file_name == "Total-Asset-Turnover.xlsx":
        indicator = "TAT"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "Total asset turnover")
        df = df.T
    elif file_name == "ROE.xlsx":
        indicator = "ROE"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "ROE")
        df = df.T
    elif file_name == "Net-Profit-Margin.xlsx":
        indicator = "NPM"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "Net profit margin")
        df = df.T
    elif file_name == "Net-Fixed-Asset-Turnover.xlsx":
        indicator = "NFAT"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "Net fixed asset turnover")
        df = df.T
    elif file_name == "Debt-to-Equity.xlsx":
        indicator = "DE"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "Debt to equity")
        df = df.T
    elif file_name == "PBV.xlsx":
        indicator = "Y"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "P/BV ratio")
        df = df.T
    elif file_name == "Payables-Turnover.xlsx":
        indicator = "PT"
        df = pandas.read_excel(file_path, skiprows=3, header=None, usecols="A:F")
        df = find_row(df, indicator, "Payables turnover")
        df = df.T
    else:
        return
    df["Company"] = company
    df["Year"] = pandas.to_datetime(df.iloc[:, 0]).dt.year
    return df[["Company", "Year", indicator]]


