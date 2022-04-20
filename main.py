import os
import pandas
import openpyxl
import matplotlib.pyplot as plt

import yfinance as yf
import pandas
import seaborn
from scipy import stats


from readers import roa, prices

df = roa.read_market_data()

result = pandas.DataFrame()
result_corr = []
for col in df.columns[1:]:
    df_part = df[["Date", col]]
    df_part = df_part.rename(columns={col: "ROA"})
    df_prices = prices.read_data(col)
    # df_part = df_part.merge(df_prices[["Date", "Adj_Close"]], on=["Date"])
    df_part = pandas.merge_asof(df_part, df_prices, left_on="Date",
                                right_on="DateNext", direction='forward')
    df_part[f"ROA_diff"] = df_part[f"ROA"].pct_change()
    df_part[f"price_diff"] = df_part[f"Adj_Close"].pct_change()
    df_part["tick"] = col
    result = pandas.concat([result, df_part])
    df_part_corr = df_part[["ROA", "Adj_Close"]].dropna(axis=0)
    result_corr.append([col, *stats.pearsonr(df_part_corr["ROA"], df_part_corr["Adj_Close"])])
print(result.head())
result = result[result["ROA_diff"] < 1]
result = result[result["ROA_diff"] > -1]
ax = seaborn.scatterplot(data=result, x="price_diff", y="ROA_diff", hue="tick")
ax.set_xlabel("Změna ceny")
ax.set_ylabel("Změna ROA")
plt.show()
result_corr = pandas.DataFrame(result_corr, columns=["tick", "ROA_price_corr", "corr_p_val"])
print(result_corr)
