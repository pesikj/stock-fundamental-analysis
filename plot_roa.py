import os
import pandas
import openpyxl
import matplotlib.pyplot as plt
import seaborn

import pandas

from readers import roa, prices

df_roa = roa.read_data("MSFT")

df_prices = prices.read_data("MSFT")
df_merged = df_roa.merge(df_prices, on=["Date"])

fig, ax = plt.subplots()
df_merged.plot(x="Date", y="ROA", ax=ax)
plt.title("Vývoj rentability aktiv společnosti Microsoft")
plt.xlabel("Datum")
plt.ylabel("Rentabilita aktiv")
plt.show()

df_merged["ROA_diff"] = df_merged["ROA"].pct_change()
df_merged["Adj_Close_diff"] = df_merged["Adj_Close"].pct_change()

plot = seaborn.scatterplot(y="ROA_diff", x="Adj_Close_diff", data=df_merged)
plot.set(title="Změna ROA vs změny hodnoty akcie společnosti Microsoft")
plot.set_xlabel("Změna ceny")
plot.set_ylabel("Změna ROA")
plt.show()


