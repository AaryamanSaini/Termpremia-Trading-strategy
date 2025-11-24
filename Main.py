import pandas as pd

# load the csv
df = pd.read_csv("ACMPREMIA.csv")

# look at the first few rows and column names
print(df.head())
print(df.columns)
