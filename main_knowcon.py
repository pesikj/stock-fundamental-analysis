import pandas
from readers import data_reader
from sklearn.linear_model import LinearRegression
import numpy
import seaborn
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats
import numpy
from scipy import stats
import pandas as pd
from scipy import stats
from linearmodels import PooledOLS
import statsmodels.api as sm

df = data_reader.read_all_indicators()
df = df[(df["CR"] != 0) & (df["DA"] != 0) & (df["RT"] != 0)]
df = df.set_index(["Company", "Year"])
df["Sector"] = df["Sector"].str.replace(" ", "_")
df =df[df["Sector"].isin(["Communication_Services", "Consumer_Cyclical", "Consumer_Defensive", "Energy", "Healthcare", "Industrials", "Technology"])]
df_ohc = pd.get_dummies(df.Sector, prefix='Sector')
# df = df[df["Sector"] == "Healthcare"]
df = df.drop(columns="Sector")

def remove_outlier_IQR(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    df_final = df[~((df[column] < (q1 - 1.5 * iqr)) | (df[column] > (q3 + 1.5 * iqr)))]
    return df_final


for i in df.columns:
    if i not in ("Year", "Company") and not i.startswith("Sector"):
        df = remove_outlier_IQR(df, i)

df.to_excel("dstest.xlsx")

for i in df.columns:
    i: str
    if i not in ("Year", "Company") and not i.startswith("Sector"):
        _, pval = stats.normaltest(df[i])
        print(f"{i} - normality test p-val = {pval}")
        df[i] = df[i].astype(float)
        # if i == "OPM":
        #     df[i] = df[i] + 1
        # # df[f"{i}_log"] = df[i].astype(float)
        # df[f"{i}_log"] = numpy.log(df[i])
        # _, pval = stats.normaltest(df[f"{i}_log"])
        # print(f"{i} - normality test p-val after log = {pval}")
        # df[f"{i}_boxcox"], fitted_lambda = stats.boxcox(df[i])
        # _, pval = stats.normaltest(df[f"{i}_boxcox"])
        # print(f"{i} - normality test p-val after box-cox = {pval}")
        df[f"{i}_johnson"], lmbda_optimal = stats.yeojohnson(df[i])
        _, pval = stats.normaltest(df[f"{i}_johnson"])
        print(f"{i} - normality test p-val after johnson = {pval}")

print(df.shape)

exog = sm.tools.tools.add_constant(df[["CR_johnson", "DA_johnson", "FL_johnson", "OPM_johnson", "RT_johnson", "TAT_johnson"]])
endog = df["Y_johnson"]

# FE und RE model
from linearmodels import PanelOLS
from linearmodels import RandomEffects

# random effects model
model_re = RandomEffects(endog, exog)
re_res = model_re.fit()
# fixed effects model
model_fe = PanelOLS(endog, exog, entity_effects=True)
fe_res = model_fe.fit()
# print results
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

df_ols = exog.merge(df_ohc, left_index=True, right_index=True)
df_ols["Y_johnson"] = df["Y_johnson"]
df_ols["const"] = 1
# df_ols = df_ols.reset_index()
columns_list = [x for x in df_ols.columns if x != "Y" and x != "Y_johnson" and x != "Company"]
equation = " + ".join(columns_list)
mod = smf.ols(formula=f"Y_johnson ~ {equation} ", data=df_ols)
res = mod.fit()
print(res.summary())

