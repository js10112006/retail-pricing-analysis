# Pricing Strategy & Revenue Optimization
### End-to-end pricing analysis on 800K+ retail transactions — elasticity modelling, revenue simulation, and an interactive recommendation engine

---

## The Business Problem

NovaBrew Online Retail (fictional company, real data) was generating strong transaction volume but revenue growth had stalled. Leadership needed answers to three questions:

- Are we leaving money on the table by underpricing certain products?
- Which products can absorb a price increase without losing customers?
- When is the right time of year to adjust prices?

This project answers all three — with data.

---

## What I Built

| Layer | What it does |
|-------|-------------|
| `data.py` | Loads, cleans, and engineers features from 1M+ raw rows |
| `2eda.py` | Exploratory analysis — revenue trends, top products, geographic breakdown |
| `analysis.py` | Price elasticity per product, revenue simulation, competitor gap analysis, seasonal effect |
| `playbook.py` | Auto-generates a business-ready pricing playbook from the analysis outputs |
| `index.html` | Interactive pricing recommendation tool — runs entirely in the browser, no server needed |

---

## Key Results

- **£17.74M** in revenue analysed across **805,549 transactions** and **5,283 products**
- Measured price elasticity for hundreds of products — identified which ones absorb price increases and which ones don't
- Built a revenue simulation that finds the optimal price point per product by modelling the demand curve
- Discovered **Q4 generates significantly higher revenue per invoice** — validated a seasonal pricing strategy
- Flagged products underpriced vs competitor benchmarks as candidates for margin expansion
- Built a live web tool where you input any product's price, competitor price, and sales volume and get a recommended price with projected revenue impact

---

## Price Elasticity — How It Works

Elasticity measures how much demand drops when price rises.

```
Elasticity = % change in quantity / % change in price

Elasticity < -1  →  Elastic   — customers are price-sensitive, tread carefully
Elasticity ≥ -1  →  Inelastic — customers tolerate price increases, pricing power exists
```

I calculated this per product using historical month-over-month price and quantity changes, then filtered to products with at least 3 valid observations to ensure statistical reliability.

---

## Revenue Simulation

For the top products, I fit a linear demand model (`Quantity ~ Price`) using scikit-learn, then simulated revenue across a range of price points to find the peak:

```python
price_range = np.linspace(current_price * 0.5, current_price * 2.0, 100)
predicted_qty = model.predict(price_range.reshape(-1, 1)).clip(0)
simulated_revenue = price_range * predicted_qty
optimal_price = price_range[np.argmax(simulated_revenue)]
```

The web tool replicates this logic client-side so anyone can interact with it in real time.

---

## Seasonal Pricing Finding

Q4 (October–December) consistently shows the highest revenue per invoice across all years in the dataset. This validates a targeted seasonal pricing strategy:

> Raise prices 5–10% on gift-oriented and home decor products in Q4. Demand is strong enough to absorb it — and historical data confirms customers spend more per order during this period.

---

## Pricing Recommendations Summary

**1. Raise prices gradually on inelastic products** — these products have pricing power. A 5% increase on the right products can expand margin with minimal demand loss.

**2. Use discounts selectively on elastic products** — blanket discounting hurts. Use promotions only where demand is provably price-sensitive and volume gain outweighs margin loss.

**3. Implement Q4 seasonal pricing** — apply a 5–10% premium on top gift products from October through December, then revert to base pricing in January.

**4. Bundle elastic with inelastic products** — pair a price-sensitive item (the hook) with a high-margin item to raise average order value while protecting margin.

**5. A/B test before full rollout** — test price changes on 10–20% of customers for 4 weeks. Measure conversion rate, units sold, and revenue per customer before committing.

---

## Project Structure

```
pricing-analysis/
├── data.py                    # cleaning + feature engineering
├── 2eda.py                    # exploratory analysis
├── analysis.py                # elasticity, simulation, competitor gap, seasonality
├── playbook.py                # generates pricing_playbook.md
├── index.html                 # interactive web tool (open directly in browser)
├── pricing_playbook.md        # full business recommendations document
├── requirements.txt
├── .gitignore
└── outputs/
    ├── revenue_by_tier.png
    ├── elasticity_distribution.png
    ├── revenue_simulation.png
    ├── competitor_gap.png
    ├── seasonal_pricing.png
    ├── product_elasticity.csv
    ├── optimal_prices.csv
    └── competitor_gap.csv
```

---

## How to Run

```bash
# 1. Clone
git clone https://github.com/yourusername/pricing-analysis
cd pricing-analysis

# 2. Set up environment
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download dataset from Kaggle and place at:
#    online_retail/online_retail_II.xlsx
#    https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci

# 5. Run in order
python data.py
python 2eda.py
python analysis.py
python playbook.py

# 6. Open the web tool
open index.html       # Mac
xdg-open index.html   # Linux
# or just double-click index.html — no server needed
```

---

## Tech Stack

`Python 3.11` · `pandas` · `numpy` · `scikit-learn` · `matplotlib` · `seaborn` · `HTML / CSS / JS` · `Chart.js`

---

## What I Would Add Next

- Real competitor pricing via web scraping (BeautifulSoup / Playwright)
- Customer segmentation by price sensitivity using RFM + clustering
- FastAPI backend to serve the pricing model as a real REST API
- Deploy web tool to Railway or Render with a live URL
- Market basket analysis to identify bundling opportunities from co-purchase data

---

## Data Source

UCI Machine Learning Repository — [Online Retail II Dataset](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci)

*NovaBrew is a fictional company. This project applies a business framing to a real public dataset for portfolio demonstration purposes.*