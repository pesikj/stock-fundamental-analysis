from readers.common import company_list_nyse, company_list_nasdaq, file_list
from readers.file_reader import read_file
import pandas


def read_single_indicator(file_name):
    df = None
    for company in company_list_nyse + company_list_nasdaq:
        if df is None:
            df = read_file(company, file_name)
        else:
            df = pandas.concat([df, read_file(company, file_name)])
    return df


def read_all_indicators():
    df = None
    for file_name in file_list:
        if df is None:
            df = read_single_indicator(file_name)
        else:
            df_new = read_single_indicator(file_name)
            df = pandas.merge(df, df_new, on=["Year", "Company"])

    companies = pandas.read_excel("Shares by industry.xlsx")
    df = df.merge(companies)
    return df
