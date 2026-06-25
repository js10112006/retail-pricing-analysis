import pandas as pd

df_2009 = pd.read_excel(
    "online_retail/online_retail_II.xlsx",
    sheet_name="Year 2009-2010"
)

df_2010 = pd.read_excel(
    "online_retail/online_retail_II.xlsx",
    sheet_name="Year 2010-2011"
)
df = pd.concat([df_2009, df_2010], ignore_index=True)
print(df.columns)
print(df.shape)
df.head()
df.info()
df.isnull().sum()
df.describe()
df = df.dropna(subset=["Description"])
df = df.dropna(subset=["Customer ID"])
df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]
df["Revenue"] = df["Quantity"] * df["Price"]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["Quarter"] = df["InvoiceDate"].dt.quarter
bad_products = [
    "Manual",
    "POSTAGE",
    "DOTCOM POSTAGE"
]

df_products = df[
    ~df["Description"].str.contains(
        "Adjustment",
        case=False,
        na=False
    )
]

df_products = df_products[
    ~df_products["Description"].isin(bad_products)
]
df_products.to_csv("clean_online_retail.csv", index=False)

print(df.shape)

print(df["Year"].value_counts())

print(df["Invoice"].nunique())

print(df["Customer ID"].nunique())

print(df["Description"].nunique())
price_variation = (
    df.groupby("Description")["Price"]
      .nunique()
      .sort_values(ascending=False)
)

print(price_variation.head(20))