import os
import pandas
import openpyxl
import matplotlib.pyplot as plt
import seaborn

import pandas

from readers import long_term_trend, prices

VALUE_NAME = "Operating profit margin"
FILE_NAME = f"OPM.xlsx"

df_roa = long_term_trend.read_data("MSFT", VALUE_NAME, FILE_NAME)

df_prices = prices.read_data("MSFT")
df_merged = pandas.merge_asof(df_roa.drop(columns=["Date"]), df_prices, left_on="DateNext", right_on="Date", direction='forward')
print(df_merged)
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.15)
if VALUE_NAME == "ROA":
    df_merged[["Net income", "Total assets"]].plot(kind="bar", ax=ax)
elif VALUE_NAME == "ROE":
    df_merged = df_merged.rename(
        columns={"Net income": "Výsledek hospodaření", "Stockholders’ equity": "Vlastní kapitál"})
    df_merged[["Výsledek hospodaření", "Vlastní kapitál"]].plot(kind="bar", ax=ax)
elif VALUE_NAME == "Operating profit margin":
    df_merged = df_merged.rename(
        columns={"Operating income": "Provozní zisk", "Revenue": "Příjmy"})
    df_merged[["Provozní zisk", "Příjmy"]].plot(kind="bar", ax=ax)
# plt.xticks(rotation = 45)
plt.ylabel("Miliardy USD")
df_merged[VALUE_NAME].plot(secondary_y=True, ax=ax)
ax.set_xticklabels(df_merged["Date"].dt.year, rotation=90)
# plt.title("Vývoj rentability aktiv společnosti Microsoft")
plt.xlabel("Rok")
if VALUE_NAME == "ROA":
    plt.ylabel("Rentabilita aktiv")
elif VALUE_NAME == "ROE":
    plt.ylabel("Rentabilita vlastního kapitálu")
elif VALUE_NAME == "Operating profit margin":
    plt.ylabel("Provozní zisková marže")
plt.show()

df_merged[f"{VALUE_NAME}_diff"] = df_merged[VALUE_NAME].pct_change()
df_merged["Adj_Close_diff"] = df_merged["Adj_Close"].pct_change()

plot = seaborn.scatterplot(y=f"{VALUE_NAME}_diff", x="Adj_Close_diff", data=df_merged)
plot.set_xlabel("Změna ceny")
if VALUE_NAME == "Operating profit margin":
    plot.set_ylabel(f"Změna provozní ziskové marže")
else:
    plot.set_ylabel(f"Změna {VALUE_NAME}")
plt.show()

fig, ax = plt.subplots()
df_merged[["Adj_Close"]].rename(columns={"Adj_Close": "Uzavírací cena"}).plot(ax=ax, kind="bar")
plt.ylabel("Miliardy USD")
df_merged[VALUE_NAME].plot(secondary_y=True, color="red")
ax.set_xticklabels(df_merged.reset_index()["Date"].dt.year, rotation=90)
# plt.title("Vývoj rentability aktiv společnosti Microsoft")
plt.xlabel("Datum")
if VALUE_NAME == "ROA":
    plt.ylabel("Rentabilita aktiv")
elif VALUE_NAME == "ROE":
    plt.ylabel("Rentabilita vlastního kapitálu")
elif VALUE_NAME == "Operating profit margin":
    plt.ylabel("Provozní zisková marže")
plt.show()