import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sklearn.linear_model import LinearRegression

# -----------------------------
# Load & Filter Data
# -----------------------------
df = pd.read_csv("clean_online_retail.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Remove non-product rows (same filters as data.py should have applied)
bad_products = ["Manual", "POSTAGE", "DOTCOM POSTAGE"]
df = df[~df["Description"].isin(bad_products)]
df = df[~df["Description"].str.contains("Adjustment", case=False, na=False)]

os.makedirs("outputs", exist_ok=True)

print("\n========== PRICING ANALYSIS ==========\n")

# -----------------------------
# Step 1 — Price Tiers
# Build categories: Budget / Mid-range / Premium
# -----------------------------
df["PriceTier"] = pd.cut(
    df["Price"],
    bins=[0, 2, 10, df["Price"].max()],
    labels=["Budget (£0–2)", "Mid-range (£2–10)", "Premium (£10+)"]
)

tier_summary = (
    df.groupby("PriceTier", observed=True)
      .agg(
          Total_Revenue=("Revenue", "sum"),
          Total_Units=("Quantity", "sum"),
          Avg_Price=("Price", "mean"),
          Num_Products=("Description", "nunique")
      )
      .reset_index()
)

print("--- Revenue by Price Tier ---")
print(tier_summary.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].bar(tier_summary["PriceTier"], tier_summary["Total_Revenue"], color=["#9FE1CB", "#1D9E75", "#085041"])
axes[0].set_title("Total Revenue by Price Tier")
axes[0].set_ylabel("Revenue (£)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))

axes[1].bar(tier_summary["PriceTier"], tier_summary["Total_Units"], color=["#B5D4F4", "#378ADD", "#0C447C"])
axes[1].set_title("Units Sold by Price Tier")
axes[1].set_ylabel("Units Sold")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

plt.tight_layout()
plt.savefig("outputs/revenue_by_tier.png")
plt.close()
print("✓ Saved: outputs/revenue_by_tier.png")

# -----------------------------
# Step 2 — Price Elasticity of Demand
# Method: group by product + month, compare price changes to quantity changes
# Elasticity = % change in quantity / % change in price
# -----------------------------

# Get products with enough price variation to measure elasticity
monthly_product = (
    df.groupby(["Description", "Year", "Month"])
      .agg(Avg_Price=("Price", "mean"), Total_Qty=("Quantity", "sum"))
      .reset_index()
      .sort_values(["Description", "Year", "Month"])
)

# Calculate period-over-period % changes within each product
monthly_product["Price_Pct_Change"] = (
    monthly_product.groupby("Description")["Avg_Price"].pct_change()
)
monthly_product["Qty_Pct_Change"] = (
    monthly_product.groupby("Description")["Total_Qty"].pct_change()
)

# Filter: only rows where price actually changed (avoid division noise)
elasticity_df = monthly_product.dropna()
elasticity_df = elasticity_df[elasticity_df["Price_Pct_Change"].abs() > 0.01]
elasticity_df = elasticity_df[elasticity_df["Price_Pct_Change"].abs() < 5]   # remove outliers

elasticity_df = elasticity_df.copy()
elasticity_df["Elasticity"] = (
    elasticity_df["Qty_Pct_Change"] / elasticity_df["Price_Pct_Change"]
)

# Summarize per product
product_elasticity = (
    elasticity_df.groupby("Description")["Elasticity"]
      .agg(["mean", "count"])
      .rename(columns={"mean": "Avg_Elasticity", "count": "Obs"})
      .query("Obs >= 3")   # need at least 3 observations to be reliable
      .reset_index()
      .sort_values("Avg_Elasticity")
)

# Classify
def classify_elasticity(e):
    if e < -1:
        return "Elastic (price-sensitive)"
    elif -1 <= e < 0:
        return "Inelastic (price-tolerant)"
    else:
        return "Unusual (positive elasticity)"

product_elasticity["Sensitivity"] = product_elasticity["Avg_Elasticity"].apply(classify_elasticity)

print("\n--- Most Price-Sensitive Products (Elastic) ---")
print(product_elasticity[product_elasticity["Avg_Elasticity"] < -1].head(10).to_string(index=False))

print("\n--- Most Price-Tolerant Products (Inelastic) ---")
inelastic = product_elasticity[
    (product_elasticity["Avg_Elasticity"] >= -1) &
    (product_elasticity["Avg_Elasticity"] < 0)
].tail(10)
print(inelastic.to_string(index=False))

# Save elasticity table
product_elasticity.to_csv("outputs/product_elasticity.csv", index=False)
print("✓ Saved: outputs/product_elasticity.csv")

# Plot: elasticity distribution
plt.figure(figsize=(12, 6))
clipped = product_elasticity["Avg_Elasticity"].clip(-10, 5)
plt.hist(clipped, bins=40, color="#7F77DD", edgecolor="white")
plt.axvline(x=-1, color="#D85A30", linestyle="--", linewidth=1.5, label="Elasticity = -1 (threshold)")
plt.axvline(x=0,  color="#888780", linestyle="--", linewidth=1,   label="Elasticity = 0")
plt.title("Price Elasticity Distribution Across Products")
plt.xlabel("Price Elasticity (clipped at ±10 for readability)")
plt.ylabel("Number of Products")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/elasticity_distribution.png")
plt.close()
print("✓ Saved: outputs/elasticity_distribution.png")

# -----------------------------
# Step 3 — Revenue Simulation (Optimal Price)
# Pick top 5 products and simulate revenue across price range
# -----------------------------

top_products = (
    df.groupby("Description")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
      .index.tolist()
)

print("\n--- Revenue Simulation: Optimal Price for Top 5 Products ---")

fig, axes = plt.subplots(1, 5, figsize=(22, 5))
optimal_prices = []

for i, product in enumerate(top_products):
    prod_df = df[df["Description"] == product].copy()

    # Fit linear model: Quantity ~ Price
    X = prod_df[["Price"]]
    y = prod_df["Quantity"]

    if len(prod_df) < 10:
        continue

    model = LinearRegression()
    model.fit(X, y)

    # Simulate revenue = price × predicted_quantity over a range of prices
    price_range = np.linspace(prod_df["Price"].min(), prod_df["Price"].max() * 1.5, 100)
    predicted_qty = model.predict(price_range.reshape(-1, 1))
    predicted_qty = np.maximum(predicted_qty, 0)   # can't sell negative units
    simulated_revenue = price_range * predicted_qty

    optimal_idx = np.argmax(simulated_revenue)
    optimal_price = price_range[optimal_idx]
    optimal_revenue = simulated_revenue[optimal_idx]
    current_price = prod_df["Price"].median()

    optimal_prices.append({
        "Product": product,
        "Current_Price": round(current_price, 2),
        "Optimal_Price": round(optimal_price, 2),
        "Simulated_Max_Revenue": round(optimal_revenue, 2)
    })

    axes[i].plot(price_range, simulated_revenue, color="#7F77DD")
    axes[i].axvline(x=optimal_price, color="#D85A30", linestyle="--", linewidth=1.2, label=f"Optimal: £{optimal_price:.2f}")
    axes[i].axvline(x=current_price, color="#1D9E75", linestyle=":", linewidth=1.2, label=f"Current: £{current_price:.2f}")
    axes[i].set_title(product[:30], fontsize=8)
    axes[i].set_xlabel("Price (£)", fontsize=8)
    axes[i].set_ylabel("Simulated Revenue (£)", fontsize=8)
    axes[i].legend(fontsize=7)
    axes[i].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))

plt.suptitle("Revenue Simulation — Optimal Price per Product", fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig("outputs/revenue_simulation.png", bbox_inches="tight")
plt.close()
print("✓ Saved: outputs/revenue_simulation.png")

optimal_df = pd.DataFrame(optimal_prices)
print(optimal_df.to_string(index=False))
optimal_df.to_csv("outputs/optimal_prices.csv", index=False)
print("✓ Saved: outputs/optimal_prices.csv")

# -----------------------------
# Step 4 — Competitor Price Gap (simulated)
# We don't have real competitor data, so we simulate it realistically:
# Competitor price = our price ± random 10–25% noise per product category
# This is standard practice for portfolio projects
# -----------------------------

np.random.seed(42)

product_avg = (
    df.groupby("Description")
      .agg(Our_Price=("Price", "median"), Revenue=("Revenue", "sum"))
      .reset_index()
)

# Simulate: competitors price ±15% on average
product_avg["Competitor_Price"] = product_avg["Our_Price"] * (
    1 + np.random.uniform(-0.25, 0.25, len(product_avg))
)
product_avg["Price_Gap"] = product_avg["Our_Price"] - product_avg["Competitor_Price"]
product_avg["Gap_Pct"] = (product_avg["Price_Gap"] / product_avg["Competitor_Price"]) * 100

# Underpriced: we charge less than competitor (opportunity to raise price)
underpriced = product_avg[product_avg["Price_Gap"] < -0.5].sort_values("Price_Gap").head(10)
# Overpriced: we charge more (risk of losing customers)
overpriced  = product_avg[product_avg["Price_Gap"] > 0.5].sort_values("Price_Gap", ascending=False).head(10)

print("\n--- Top 10 Underpriced Products (Opportunity to raise price) ---")
print(underpriced[["Description", "Our_Price", "Competitor_Price", "Gap_Pct"]].to_string(index=False))

print("\n--- Top 10 Overpriced Products (Risk of losing customers) ---")
print(overpriced[["Description", "Our_Price", "Competitor_Price", "Gap_Pct"]].to_string(index=False))

product_avg.to_csv("outputs/competitor_gap.csv", index=False)
print("✓ Saved: outputs/competitor_gap.csv")

# Plot: price gap scatter (our price vs competitor price, top 200 by revenue)
top200 = product_avg.nlargest(200, "Revenue")

plt.figure(figsize=(10, 8))
plt.scatter(top200["Our_Price"], top200["Competitor_Price"],
            c=top200["Gap_Pct"], cmap="RdYlGn_r", alpha=0.7, s=60)
plt.plot([0, top200["Our_Price"].max()], [0, top200["Our_Price"].max()],
         color="#888780", linestyle="--", linewidth=1, label="Equal pricing line")
plt.colorbar(label="Price Gap % (red = we are more expensive)")
plt.title("Our Price vs Simulated Competitor Price\n(Top 200 products by revenue)")
plt.xlabel("Our Price (£)")
plt.ylabel("Competitor Price (£)")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/competitor_gap.png")
plt.close()
print("✓ Saved: outputs/competitor_gap.png")

# -----------------------------
# Step 5 — Seasonal Price Effect
# Does revenue change by quarter independent of volume?
# -----------------------------
seasonal = (
    df.groupby("Quarter")
      .agg(Avg_Price=("Price", "mean"), Avg_Revenue_per_Invoice=("Revenue", "mean"))
      .reset_index()
)

print("\n--- Seasonal Pricing Effect ---")
print(seasonal.to_string(index=False))

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

ax1.bar(seasonal["Quarter"], seasonal["Avg_Price"], color="#7F77DD", alpha=0.7, label="Avg Price")
ax2.plot(seasonal["Quarter"], seasonal["Avg_Revenue_per_Invoice"],
         color="#D85A30", marker="o", linewidth=2, label="Avg Revenue/Invoice")

ax1.set_xlabel("Quarter")
ax1.set_ylabel("Average Price (£)", color="#7F77DD")
ax2.set_ylabel("Avg Revenue per Invoice (£)", color="#D85A30")
ax1.set_xticks([1, 2, 3, 4])
ax1.set_xticklabels(["Q1", "Q2", "Q3", "Q4"])

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("Seasonal Effect on Pricing and Revenue")
plt.tight_layout()
plt.savefig("outputs/seasonal_pricing.png")
plt.close()
print("✓ Saved: outputs/seasonal_pricing.png")

print("\n========== ANALYSIS COMPLETE ==========")
print("Outputs saved to the 'outputs' folder.")
print("Next step: run playbook.py to generate recommendations.")