import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Avoid hardcoded paths - use pathlib to locate root dynamically
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. SETUP PARAMETERS FOR THE PROJECTION
np.random.seed(42)
n_simulations = 1000       # Number of random asset paths to calculate
n_years = 5                # Project timeline
trading_days_per_year = 252
total_days = n_years * trading_days_per_year

# Assuming standard historical market traits for a diversified equity fund
initial_nav = 100.0        # Starting baseline NAV price
annual_mu = 0.12           # 12% Expected Annual Return (Drift)
annual_sigma = 0.15        # 15% Annual Volatility (Diffusion)

# Scale parameter distributions down to daily intervals
daily_mu = annual_mu / trading_days_per_year
daily_sigma = annual_sigma / np.sqrt(trading_days_per_year)

# 2. RUN SIMULATION LOOPS (Geometric Brownian Motion)
# Matrix shape: (days, simulations)
nav_matrix = np.zeros((total_days, n_simulations))
nav_matrix[0] = initial_nav

for t in range(1, total_days):
    # Random shocks from normal distribution
    shocks = np.random.normal(0, 1, n_simulations)
    # Price compounding formula: S_t = S_{t-1} * exp((mu - 0.5*sigma^2) + sigma * Z)
    nav_matrix[t] = nav_matrix[t-1] * np.exp((daily_mu - 0.5 * daily_sigma**2) + daily_sigma * shocks)

# 3. EXTRACT STATISTICAL UNCERTAINTY BANDS
timeline = np.arange(total_days) / trading_days_per_year  # Convert x-axis indices back to year units
p95 = np.percentile(nav_matrix, 95, axis=1)  # Optimistic Target (Top 5%)
p50 = np.percentile(nav_matrix, 50, axis=1)  # Median Expectation (Most likely)
p5 = np.percentile(nav_matrix, 5, axis=1)    # Conservative Floor (Worst 5% market stress)

# 4. PLOT OUT THE VISUAL RESULTS
plt.figure(figsize=(10, 6))

# Plot a small transparent sample of actual individual simulated paths
plt.plot(timeline, nav_matrix[:, :15], color="gray", alpha=0.15)

# Plot the heavy structural tracking boundaries
plt.plot(timeline, p50, color="#1f77b4", lw=2.5, label="Median Path (50th Percentile)")
plt.plot(timeline, p95, color="#2ca02c", lw=1.5, linestyle="--", label="Optimistic Boundary (95th Percentile)")
plt.plot(timeline, p5, color="#d62728", lw=1.5, linestyle="--", label="Downside Floor (5th Percentile)")

# Fill the uncertainty bands with shading
plt.fill_between(timeline, p5, p95, color="#1f77b4", alpha=0.1, label="90% Confidence Interval")

plt.title("5-Year Mutual Fund NAV Growth Projection (Monte Carlo Simulation Analysis)")
plt.xlabel("Years Implemented")
plt.ylabel("Projected NAV Price (INR)")
plt.legend(loc="upper left")
plt.grid(True, linestyle="--", alpha=0.5)

# Save image into designated output path asset area cleanly
chart_path = OUTPUT_DIR / "monte_carlo_projection.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"🔥 Bonus B3 Complete! Chart successfully output to: {chart_path}")
print(f"📈 Summary Statistics (Year 5 Final Prices):")
print(f"   - Optimistic Target (95th): INR {p95[-1]:.2f}")
print(f"   - Median Projection (50th): INR {p50[-1]:.2f}")
print(f"   - Downside Risk Floor (5th): INR {p5[-1]:.2f}")