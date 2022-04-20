import os
import pandas
import openpyxl
import matplotlib.pyplot as plt
import seaborn

import pandas

from readers import roa, prices

df_roa = roa.read_data("MSFT")

df_prices = prices.read_data("MSFT")
df_merged = pandas.merge_asof(df_roa.drop(columns=["Date"]), df_prices, left_on="DateNext", right_on="Date", direction='forward')
print(df_merged)
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.15)
df_merged[["Net income", "Total assets"]].plot(kind="bar", ax=ax)
# plt.xticks(rotation = 45)
plt.ylabel("Miliardy USD")
df_merged["ROA"].plot(secondary_y=True, ax=ax)
ax.set_xticklabels(df_merged["Date"].dt.year, rotation=90)
# plt.title("Vývoj rentability aktiv společnosti Microsoft")
plt.xlabel("Datum")
plt.ylabel("Rentabilita aktiv")
plt.show()

df_merged["ROA_diff"] = df_merged["ROA"].pct_change()
df_merged["Adj_Close_diff"] = df_merged["Adj_Close"].pct_change()

plot = seaborn.scatterplot(y="ROA_diff", x="Adj_Close_diff", data=df_merged)
# plot.set(title="Změna ROA vs změny hodnoty akcie společnosti Microsoft")
plot.set_xlabel("Změna ceny")
plot.set_ylabel("Změna ROA")
plt.show()

fig, ax = plt.subplots()
# plt.subplots_adjust(left=0.15)
# df_merged.plot(x="Date", y="ROA", ax=ax)
df_merged[["Adj_Close"]].rename(columns={"Adj_Close": "Uzavírací cena"}).plot(ax=ax, kind="bar")
plt.ylabel("Miliardy USD")
df_merged["ROA"].plot(secondary_y=True, color="red")
ax.set_xticklabels(df_merged.reset_index()["Date"].dt.year, rotation=90)
# plt.title("Vývoj rentability aktiv společnosti Microsoft")
plt.xlabel("Datum")
plt.ylabel("Rentabilita aktiv")
plt.show()