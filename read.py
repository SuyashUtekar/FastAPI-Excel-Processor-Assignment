import pandas as pd

df = pd.read_excel("test_data/capbudg.xls", header=None, engine="xlrd")

# Print first 30 rows to understand the layout
pd.set_option("display.max_rows", 30)
print(df.head(30))
