import os
import pandas
import openpyxl
import matplotlib.pyplot as plt

import yfinance as yf
import pandas
import seaborn

from readers import roa, prices

df = roa.read_market_data()

result = pandas.DataFrame()
result_corr = []
for col in df.columns[1:]:
    df_part = df[["Date", col]]
    df_part = df_part.rename(columns={col: f"ROA"})
    df_prices = prices.read_data(col)
    df_part = df_part.merge(df_prices[["Date", "Adj_Close"]], on=["Date"])
    df_part[f"ROA_diff"] = df_part[f"ROA"].pct_change()
    df_part[f"price_diff"] = df_part[f"Adj_Close"].pct_change()
    df_part["tick"] = col
    result = pandas.concat([result, df_part])
    result_corr.append([col, df_part[f"ROA_diff"].corr(df_part[f"price_diff"])])
print(result.head())
result = result[result["ROA_diff"] < 1]
result = result[result["ROA_diff"] > -1]
ax = seaborn.scatterplot(data=result, x="price_diff", y="ROA_diff", hue="tick")
ax.set_xlabel("Změna ceny")
ax.set_ylabel("Změna ROA")
plt.show()
result_corr = pandas.DataFrame(result_corr, columns=["tick", "ROA_price_corr"])
print(result_corr)
