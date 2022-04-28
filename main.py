import pandas
from readers import regression_market_models
from sklearn.linear_model import LinearRegression
import numpy
import seaborn
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

VALUES_TO_PROCESS = [
    ["Cash-Ratio.xlsx", "CashRatio"],
    ["CTR.xlsx", "CTR"],
    ["Current-Ratio.xlsx", "CurrentRatio"],
    ["Debt-to-Assets.xlsx", "DebtToAssets"],
    ["Debt-to-Capital.xlsx", "DebtToCapital"],
    ["Debt-to-Equity.xlsx", "DebtToEquity"],
    ["Economic-Profit-Margin.xlsx", "EconomicProfitMargin"],
    ["Economic-Spread.xlsx", "EconomicSpread"],
    ["Financial-Leverage.xlsx", "FinancialLeverage"],
    ["Fixed-Charge-Coverage.xlsx", "FixedChargeCoverage"],
    ["Gross-Profit-Margin.xlsx", "Gross-Profit-Margin"],
    ["Interest-Coverage.xlsx", "Interest-Coverage"],
    ["MVA-Margin.xlsx", "MVAMargin"],
    ["MVA-Spread.xlsx", "MVA-Spread"],
    ["Net-Fixed-Asset-Turnover.xlsx", "NetFixedAssetTurnover"],
    ["Net-Profit-Margin.xlsx", "NetProfitMargin"],
    ["Operating-Profit-Margin.xlsx", "OperatingProfitMargin"],
    ["Payables-Turnover.xlsx", "Payables-Turnover"],
    ["Quick-Ratio.xlsx", "Quick-Ratio"],
    ["PBV.xlsx", "PBV"],
    ["Receivables-Turnover.xlsx", "ReceivablesTurnover"],
    ["ROA2.xlsx", "ROA"],
    ["ROE2.xlsx", "ROE2"],
    ["ROIC.xlsx", "ROIC"],
    ["TO.xlsx", "TO"],
    ["Total-Asset-Turnover.xlsx", "TotalAssetTurnover"],
    ["Working-Capital-Turnover.xlsx", "WorkingCapitalTurnover"]
]

df = regression_market_models.read_market_data(VALUES_TO_PROCESS)
df = df[df["CashRatio"] > 0]

selected_indicators = ["CurrentRatio", "DebtToAssets", "FinancialLeverage", "FixedChargeCoverage", "MVAMargin",
                       "OperatingProfitMargin", "ReceivablesTurnover", "TotalAssetTurnover", "Date", "PBV"]

df = df[selected_indicators]

corr = df.corr()
corr.to_excel("corr.xlsx")
mask = numpy.triu(numpy.ones_like(corr, dtype=bool))
f, ax = plt.subplots(figsize=(11, 9))
cmap = seaborn.diverging_palette(230, 20, as_cmap=True)
seaborn.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
plt.show()



# df_one_hot = pandas.get_dummies(df.Company, prefix='Company')
# df_one_hot["Company"] = df["Company"]
# df = pandas.merge(df, df_one_hot, on="Company")

df["Year"] = df["Date"].dt.year
# equation = [f"{column} + " for column in df.columns if column.startswith("Company_")]
# equation = "".join(equation)

df = df[df["Year"] == 2021]
equation = " + ".join(selected_indicators[:-2])
mod = smf.ols(formula=f"PBV ~ {equation} ", data=df)
res = mod.fit()
print(res.summary())


mod = smf.ols(formula=f"PBV ~ MVAMargin + OperatingProfitMargin", data=df)
res = mod.fit()
print(res.summary())