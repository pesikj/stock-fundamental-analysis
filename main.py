from readers import regression_market_models

VALUES_TO_PROCESS = [
    ["Economic-Profit-Margin.xlsx", "Economic profit margin"],
    ["ROA2.xlsx", "ROA"],
]

df = regression_market_models.read_market_data(VALUES_TO_PROCESS)

print(df)
df.to_excel("df.xlsx")
