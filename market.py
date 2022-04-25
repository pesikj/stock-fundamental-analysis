import matplotlib.pyplot as plt
import numpy
import pandas
import seaborn
from scipy import stats

from readers import long_term_trend, prices

VALUE_NAME = "ROE"
FILE_NAME = f"ROE.xlsx"

df = long_term_trend.read_market_data(FILE_NAME)

result = pandas.DataFrame()
result_corr = []
result_norm = []
index = 0
fig, ax = plt.subplots(figsize=(12,8))
for col in df.columns[1:]:
    index += 1
    df_part = df[["Date", col]]
    df_part = df_part.rename(columns={col: VALUE_NAME})
    df_prices = prices.read_data(col)
    # df_part = df_part.merge(df_prices[["Date", "Adj_Close"]], on=["Date"])
    df_part = pandas.merge_asof(df_part, df_prices, left_on="Date",
                                right_on="DateNext", direction='forward')
    df_part[f"{VALUE_NAME}_diff"] = df_part[VALUE_NAME].pct_change()
    df_part["price_diff"] = df_part["Adj_Close"].pct_change()
    df_part["tick"] = col
    result = pandas.concat([result, df_part])
    df_part_corr = df_part[[f"{VALUE_NAME}_diff", "price_diff"]].replace(-numpy.inf, None).replace(numpy.inf, None).dropna(axis=0)
    ROA_price_norm_pval = stats.shapiro(df_part_corr[f"{VALUE_NAME}_diff"])[1]
    price_norm_pval = stats.shapiro(df_part_corr["price_diff"])[1]
    if ROA_price_norm_pval > 0.05 and price_norm_pval > 0.05:
        result_corr.append([col, "Pearsonův", *stats.pearsonr(df_part_corr[f"{VALUE_NAME}_diff"], df_part_corr["price_diff"])])
    else:
        result_corr.append([col, "Kendallovo tau", *stats.kendalltau(df_part_corr[f"{VALUE_NAME}_diff"], df_part_corr["price_diff"])])
    result_norm.append([col, ROA_price_norm_pval, price_norm_pval])
result = result[result[f"{VALUE_NAME}_diff"] < 1]
result = result[result[f"{VALUE_NAME}_diff"] > -1]

seaborn.set(font_scale=1.5)


ax = seaborn.relplot(data=result[result["tick"].isin(df.columns[1:9])].rename(
    columns={f"{VALUE_NAME}_diff": f"Změna {VALUE_NAME}", "price_diff": "Změna ceny"}),
                     x="Změna ceny", y=f"Změna {VALUE_NAME}", col="tick", col_wrap=4)
ax = seaborn.relplot(data=result[result["tick"].isin(df.columns[9:])].rename(
    columns={f"{VALUE_NAME}_diff": f"Změna {VALUE_NAME}", "price_diff": "Změna ceny"}),
                     x="Změna ceny", y=f"Změna {VALUE_NAME}", col="tick", col_wrap=4)
plt.show()
result_corr = pandas.DataFrame(result_corr, columns=["firma", "Koeficient", "Koeficient", "p-hodnota"])
print(result_corr)
result_norm = pandas.DataFrame(result_norm, columns=["tick", f"{VALUE_NAME}_price_norm_pval", "price_norm_pval"])
print(result_norm)
result_corr.to_excel(f"output/{VALUE_NAME}_corr.xlsx", index=False)
