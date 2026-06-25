import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("clean_online_retail.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# -----------------------------
# Create Output Folder
# -----------------------------
os.makedirs("outputs", exist_ok=True)

# -----------------------------
# Total Revenue
# -----------------------------
total_revenue = df["Revenue"].sum()

print("\n========== BUSINESS SUMMARY ==========")
print(f"Total Revenue: £{total_revenue:,.2f}")
print(f"Total Transactions: {len(df):,}")
print(f"Unique Customers: {df['Customer ID'].nunique():,}")
print(f"Unique Products: {df['Description'].nunique():,}")
print("======================================\n")

# -----------------------------
# Monthly Revenue Trend
# -----------------------------
monthly_revenue = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["Revenue"]
      .sum()
)

plt.figure(figsize=(14, 6))
plt.plot(
    monthly_revenue.index.astype(str),
    monthly_revenue.values,
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig("outputs/monthly_revenue.png")
plt.close()

print("✓ Saved: outputs/monthly_revenue.png")

# -----------------------------
# Top 20 Products by Revenue
# -----------------------------
top_products = (
    df.groupby("Description")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(20)
)

print("\nTop 20 Products By Revenue:")
print(top_products)

plt.figure(figsize=(14, 8))
plt.bar(top_products.index, top_products.values)

plt.title("Top 20 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=90)

plt.tight_layout()

plt.savefig("outputs/top_products.png")
plt.close()

print("✓ Saved: outputs/top_products.png")

# -----------------------------
# Top 10 Countries by Revenue
# -----------------------------
country_revenue = (
    df.groupby("Country")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\nTop Countries By Revenue:")
print(country_revenue)

plt.figure(figsize=(12, 6))
plt.bar(country_revenue.index, country_revenue.values)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Country")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/top_countries.png")
plt.close()

print("✓ Saved: outputs/top_countries.png")

# -----------------------------
# Price Distribution
# -----------------------------
plt.figure(figsize=(12, 6))

sns.histplot(
    df["Price"],
    bins=50,
    kde=True
)

plt.title("Price Distribution")
plt.xlabel("Price (£)")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig("outputs/price_distribution.png")
plt.close()

print("✓ Saved: outputs/price_distribution.png")

# -----------------------------
# Revenue Distribution
# -----------------------------
plt.figure(figsize=(12, 6))

sns.histplot(
    df["Revenue"],
    bins=50,
    kde=True
)

plt.title("Revenue Distribution")
plt.xlabel("Revenue (£)")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig("outputs/revenue_distribution.png")
plt.close()

print("✓ Saved: outputs/revenue_distribution.png")

# -----------------------------
# Top Customers
# -----------------------------
customer_revenue = (
    df.groupby("Customer ID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(20)
)

print("\nTop 20 Customers By Revenue:")
print(customer_revenue)

plt.figure(figsize=(14, 6))

plt.bar(
    customer_revenue.index.astype(str),
    customer_revenue.values
)

plt.title("Top 20 Customers by Revenue")
plt.xlabel("Customer ID")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=90)

plt.tight_layout()

plt.savefig("outputs/top_customers.png")
plt.close()

print("✓ Saved: outputs/top_customers.png")

print("\nEDA completed successfully.")
print("All charts saved inside the 'outputs' folder.")