from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Avoid hardcoded paths - dynamic lookups via pathlib
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. GENERATE REPLICABLE HISTORICAL TRACK DATA FOR 5 FUNDS
np.random.seed(101)
funds = ["Fund_A", "Fund_B", "Fund_C", "Fund_D", "Fund_E"]
n_funds = len(funds)
n_obs = 1000

# Generating stylized, correlated continuous daily returns
mean_returns = np.array([0.14, 0.11, 0.13, 0.09, 0.12]) / 252  # Annualized down to daily return space
cov_matrix = np.array([
    [0.0003, 0.0001, 0.00015, 0.00005, 0.0001],
    [0.0001, 0.0002, 0.00008, 0.00004, 0.00007],
    [0.00015, 0.00008, 0.00025, 0.00006, 0.00012],
    [0.00005, 0.00004, 0.00006, 0.00015, 0.00005],
    [0.0001, 0.00007, 0.00012, 0.00005, 0.00022]
])

daily_returns = np.random.multivariate_normal(mean_returns, cov_matrix, n_obs)
df_returns = pd.DataFrame(daily_returns, columns=funds)

# 2. CALCULATE LOGISTIC ANNUALIZED METRICS
annual_returns = df_returns.mean() * 252
annual_cov = df_returns.cov() * 252
risk_free_rate = 0.05  # Standard 5% Risk-Free Baseline Rate (e.g., Govt T-Bills)

# 3. MONTE CARLO RANDOM WEIGHT ALLOCATION PORTFOLIO GENERATION
n_portfolios = 5000
results = np.zeros((3 + n_funds, n_portfolios))

for i in range(n_portfolios):
    weights = np.random.random(n_funds)
    weights /= np.sum(weights)  # Capital allocation constraint: Sum of weights must equal 1.0 (100%)
    
    # Portfolio expected return and volatility metrics
    p_return = np.sum(weights * annual_returns)
    p_volatility = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))
    
    # Calculate Sharpe Ratio
    p_sharpe = (p_return - risk_free_rate) / p_volatility
    
    results[0, i] = p_return
    results[1, i] = p_volatility
    results[2, i] = p_sharpe
    for j in range(len(weights)):
        results[3 + j, i] = weights[j]

# Convert statistical arrays out to a structured framework
columns = ["Return", "Volatility", "Sharpe"] + [f"{f}_Weight" for f in funds]
df_portfolios = pd.DataFrame(results.T, columns=columns)

# 4. ISOLATE KEY BENCHMARK MODEL BOUNDARIES
max_sharpe_idx = df_portfolios["Sharpe"].idxmax()
max_sharpe_portfolio = df_portfolios.iloc[max_sharpe_idx]

min_vol_idx = df_portfolios["Volatility"].idxmin()
min_vol_portfolio = df_portfolios.iloc[min_vol_idx]

# 5. GENERATE THE EFFICIENT FRONTIER VISUAL SCATTER PLOT
plt.figure(figsize=(10, 6))
sc = plt.scatter(df_portfolios["Volatility"], df_portfolios["Return"], c=df_portfolios["Sharpe"], cmap="viridis", marker="o", s=10, alpha=0.4)
plt.colorbar(sc, label="Sharpe Ratio")

# Highlight Maximum Sharpe Ratio Allocation Target
plt.scatter(max_sharpe_portfolio["Volatility"], max_sharpe_portfolio["Return"], color="red", marker="*", s=200, label="Max Sharpe Ratio (Optimal Portfolio)")

# Highlight Minimum Variance Allocation Target
plt.scatter(min_vol_portfolio["Volatility"], min_vol_portfolio["Return"], color="darkorange", marker="X", s=150, label="Minimum Variance Portfolio")

plt.title("Markowitz Modern Portfolio Theory: Efficient Frontier Optimization")
plt.xlabel("Annualized Volatility / Portfolio Risk (Standard Deviation)")
plt.ylabel("Expected Annualized Portfolio Return")
plt.legend(loc="upper left")
plt.grid(True, linestyle="--", alpha=0.5)

chart_path = OUTPUT_DIR / "efficient_frontier.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

# 6. OUTPUT STRATEGY SPECIFICATION TO SYSTEM TERMINAL
print(f"🔥 Bonus B4 Complete! Efficient Frontier chart saved to: {chart_path}")
print(f"\n💡 MAXIMUM SHARPE RATIO OPTIMAL WEIGHT ALLOCATION:")
print(f"   - Expected Return: {max_sharpe_portfolio['Return']*100:.2f}%")
print(f"   - Volatility Risk: {max_sharpe_portfolio['Volatility']*100:.2f}%")
print(f"   - Max Sharpe Metrics: {max_sharpe_portfolio['Sharpe']:.2f}")
print("   - Allocations:")
for f in funds:
    print(f"     * {f}: {max_sharpe_portfolio[f'{f}_Weight']*100:.1f}%")