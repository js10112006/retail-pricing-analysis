

# Pricing Strategy & Revenue Optimization Analysis

## Executive Summary

This project analyzes pricing performance using the Online Retail II dataset containing over 800,000 retail transactions and £17.7 million in revenue.

The objective was to understand how pricing impacts demand, identify revenue optimization opportunities, estimate product-level price elasticity, and provide business-focused pricing recommendations.

### Key Results

* Analyzed 805,549 transactions across 5,283 products.
* Generated £17.74 million in total revenue.
* Identified products with highly elastic and inelastic demand.
* Simulated revenue-maximizing price points for top-selling products.
* Evaluated seasonal pricing opportunities.
* Developed competitor benchmarking scenarios for pricing decisions.

---

# Business Context

### Company

NovaBrew Online Retail (fictional business based on real retail transaction data)

### Business Problem

Revenue growth has slowed despite strong transaction volume. Leadership suspects current pricing may not be optimized across product categories.

### Objectives

* Measure demand sensitivity to price changes.
* Identify products suitable for price increases.
* Detect products requiring promotional pricing.
* Analyze seasonal pricing opportunities.
* Provide actionable pricing recommendations.

---

# Dataset Overview

| Metric             | Value       |
| ------------------ | ----------- |
| Total Transactions | 805,549     |
| Unique Customers   | 5,878       |
| Unique Products    | 5,283       |
| Total Revenue      | £17,743,429 |
| Countries          | 40+         |

### Data Source

Online Retail II Dataset (UCI / Kaggle)

### Data Preparation

The following preprocessing steps were performed:

* Removed cancelled orders
* Removed returns and negative quantities
* Removed invalid pricing records
* Removed missing customer records where required
* Created Revenue feature
* Extracted Month, Year and Quarter attributes

---

# Exploratory Data Analysis

## Revenue Overview

Total revenue generated during the analysis period exceeded £17.7 million.

The business demonstrates strong product diversity with more than 5,000 unique products and nearly 6,000 customers.

---

## Geographic Revenue Distribution

The United Kingdom accounted for approximately 83% of total revenue.

Top revenue-generating countries:

1. United Kingdom
2. EIRE
3. Netherlands
4. Germany
5. France

### Business Implication

The company is heavily dependent on a single market and may benefit from geographic diversification.

---

## Product Revenue Analysis

The highest revenue-generating products included:

* REGENCY CAKESTAND 3 TIER
* WHITE HANGING HEART T-LIGHT HOLDER
* JUMBO BAG RED RETROSPOT
* ASSORTED COLOUR BIRD ORNAMENT

### Business Implication

A small subset of products contributes a disproportionately large share of revenue.

These products should receive priority pricing analysis.

---

# Price Elasticity Analysis

## Objective

Determine how sensitive customer demand is to price changes.

Elasticity was estimated using historical price and quantity relationships at the product level.

### Interpretation

| Elasticity       | Interpretation      |
| ---------------- | ------------------- |
| Less than -1     | Elastic demand      |
| Between -1 and 0 | Inelastic demand    |
| Near 0           | Very price tolerant |

---

## Findings

* Most products exhibit elastic demand.
* A smaller subset demonstrates inelastic demand.
* Inelastic products represent opportunities for gradual price increases.

### Business Implication

Products with low price sensitivity provide pricing power and margin expansion opportunities.

---

# Revenue Optimization Simulation

Revenue simulations were performed on the highest-revenue products by evaluating multiple possible price points and estimating resulting revenue.

## Example Findings

| Product                            | Current Price | Recommended Price  |
| ---------------------------------- | ------------- | ------------------ |
| REGENCY CAKESTAND 3 TIER           | £12.75        | Scenario-dependent |
| WHITE HANGING HEART T-LIGHT HOLDER | £2.95         | Scenario-dependent |
| JUMBO BAG RED RETROSPOT            | £1.95         | Scenario-dependent |

### Recommendation

All pricing changes should be validated using controlled A/B testing before rollout.

---

# Seasonal Pricing Analysis

Quarterly revenue analysis reveals strong seasonality.

### Observation

Q4 consistently generates the highest revenue.

### Recommendation

Implement seasonal premium pricing strategies during peak holiday periods.

Suggested increase:

* 5% to 10% on gift-oriented products during Q4

---

# Competitor Benchmarking Scenario

A scenario analysis was performed using simulated competitor pricing benchmarks.

### Purpose

Evaluate how pricing decisions may change when competitors operate at different price levels.

### Insights

* Several products appear underpriced relative to benchmark competitors.
* Some premium products may be vulnerable to competitive pricing pressure.

### Limitation

This analysis uses simulated competitor data and should not be interpreted as actual market pricing.

Future work should incorporate real competitor pricing obtained through APIs or web scraping.

---

# Business Recommendations

## Recommendation 1

Increase prices gradually on low-elasticity products.

Expected Outcome:

* Higher margins
* Minimal reduction in demand

---

## Recommendation 2

Use discounts strategically on highly elastic products.

Expected Outcome:

* Increased sales volume
* Improved inventory movement

---

## Recommendation 3

Implement seasonal pricing during Q4.

Expected Outcome:

* Improved holiday-period profitability

---

## Recommendation 4

Bundle complementary products.

Expected Outcome:

* Higher average order value
* Improved cross-selling performance

---

## Recommendation 5

Introduce A/B testing before large-scale pricing changes.

Expected Outcome:

* Reduced pricing risk
* Data-driven pricing decisions

---

# Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-Learn
* Power BI

---

# Future Improvements

* Real competitor pricing integration
* Dynamic pricing engine
* Customer segmentation (RFM)
* Market basket analysis
* Predictive demand forecasting

---

# Conclusion

This project demonstrates how data-driven pricing strategies can support revenue optimization and business growth.

Through elasticity estimation, revenue simulation, seasonal analysis, and pricing recommendations, the analysis provides a framework for making informed pricing decisions in a retail environment.
