import pandas
from readers import regression_market_models
from sklearn.linear_model import LinearRegression
import numpy
import seaborn
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats
import numpy
import pandas as pd

from linearmodels import PooledOLS
import statsmodels.api as sm

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

def create_correlation_plot(df, annot=False):
    corr = df.corr()
    corr.to_excel("corr.xlsx")
    mask = numpy.triu(numpy.ones_like(corr, dtype=bool))
    f, ax = plt.subplots(figsize=(11, 9))
    cmap = seaborn.diverging_palette(230, 20, as_cmap=True)
    seaborn.heatmap(corr, mask=mask, cmap=cmap, vmax=0.8, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=annot)
    plt.show()


create_correlation_plot(df)
selected_indicators = ["CurrentRatio", "DebtToAssets", "FinancialLeverage",
                       "OperatingProfitMargin", "ReceivablesTurnover", "TotalAssetTurnover", "Date", "PBV", "Company"]
df = df[selected_indicators]
create_correlation_plot(df.iloc[:, :-1], True)
df = df.rename(columns={"CurrentRatio": "CR", "DebtToAssets": "DA", "FinancialLeverage": "FL", "OperatingProfitMargin": "OPM", "ReceivablesTurnover": "RT", "TotalAssetTurnover": "TAT"})

# df_one_hot = pandas.get_dummies(df.Company, prefix='Company')
# df_one_hot["Company"] = df["Company"]
# df = pandas.merge(df, df_one_hot, on="Company")

df["Year"] = df["Date"].dt.year
df = df.drop("Date", axis=1)
for i in df.columns:
    if i not in ("Date", "Year", "Company"):
        _, pval = stats.normaltest(df[i])
        if pval < 0.05:
            df[i] = numpy.log(df[i])
        _, pval = stats.normaltest(df[i])
# df = df[df["Year"] == 2021]
equation = " + ".join(df.columns[:-3])
mod = smf.ols(formula=f"PBV ~ {equation} ", data=df)
res = mod.fit()

df = df.dropna(axis=0)
dataset: pandas.DataFrame = df
dataset = dataset.set_index(["Company", "Year"])
years = dataset.index.get_level_values("Year").to_list()
dataset["year"] = pandas.Categorical(years)

# FE und RE model
from linearmodels import PanelOLS
from linearmodels import RandomEffects
exog = sm.tools.tools.add_constant(dataset[["FL", "OPM", "TAT"]])
endog = dataset["PBV"]


mod = PooledOLS(endog, exog)
pooledOLS_res = mod.fit(cov_type='clustered', cluster_entity=True)
# Store values for checking homoskedasticity graphically
fittedvals_pooled_OLS = pooledOLS_res.predict().fitted_values
residuals_pooled_OLS = pooledOLS_res.resids

# 3A. Homoskedasticity
import matplotlib.pyplot as plt
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_pooled_OLS, residuals_pooled_OLS, color = "blue")
ax.axhline(0, color = 'r', ls = '--')
ax.set_xlabel("Predikované hodnoty")
ax.set_ylabel("Residua")
plt.show()

# 3A.2 White-Test
from statsmodels.stats.diagnostic import het_white, het_breuschpagan
pooled_OLS_dataset = pd.concat([dataset, residuals_pooled_OLS], axis=1)
pooled_OLS_dataset = pooled_OLS_dataset.drop(["year"], axis = 1).fillna(0)

white_test_results = het_white(pooled_OLS_dataset["residual"], exog)
labels = ["LM-Stat", "LM p-val", "F-Stat", "F p-val"] 
print(dict(zip(labels, white_test_results)))
# 3A.3 Breusch-Pagan-Test
breusch_pagan_test_results = het_breuschpagan(pooled_OLS_dataset["residual"], exog)
labels = ["LM-Stat", "LM p-val", "F-Stat", "F p-val"] 
print(dict(zip(labels, breusch_pagan_test_results)))

from statsmodels.stats.stattools import durbin_watson

durbin_watson_test_results = durbin_watson(pooled_OLS_dataset["residual"])
print(durbin_watson_test_results)

# FE und RE model
from linearmodels import PanelOLS
from linearmodels import RandomEffects
# random effects model
model_re = RandomEffects(endog, exog)
re_res = model_re.fit()
# fixed effects model
model_fe = PanelOLS(endog, exog, entity_effects = True)
fe_res = model_fe.fit()
#print results
print(re_res)
print(fe_res)

import numpy.linalg as la
from scipy import stats
import numpy as np


def hausman(fe, re):
    b = fe.params
    B = re.params
    v_b = fe.cov
    v_B = re.cov
    df = b[np.abs(b) < 1e8].size
    chi2 = np.dot((b - B).T, la.inv(v_b - v_B).dot(b - B))
    
    pval = stats.chi2.sf(chi2, df)
    return chi2, df, pval

hausman_results = hausman(fe_res, re_res)
print("chi - Squared: " + str(hausman_results[0]))
print("degrees of freedom: " + str(hausman_results[1]))
print("p - Value: " + str(hausman_results[2]))
