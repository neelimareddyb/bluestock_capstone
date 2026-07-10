import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. SETUP & SIMULATED DATABASES
np.random.seed(42)
funds = [f"Fund_{i}" for i in range(1, 41)]
categories = ["Large Cap", "Mid Cap", "Small Cap", "Flexi Cap"]
risk_grades = ["Low", "Moderate", "High"]

# 252 trading days for 40 funds
dates = pd.date_range(start="2025-01-01", periods=252, freq="B")
returns_data = {fund: np.random.normal(0.0005, 0.012, len(dates)) for fund in funds}
df_returns = pd.DataFrame(returns_data, index=dates)

# TASK 1: HISTORICAL VaR (95%) & CVaR (EXPECTED SHORTFALL)
var_results = []
for fund in df_returns.columns:
    var_95 = np.percentile(df_returns[fund], 5)
    cvar_95 = df_returns[fund][df_returns[fund] <= var_95].mean()
    var_results.append({"Fund_Name": fund, "VaR_95": var_95, "CVaR_95": cvar_95})

df_var_report = pd.DataFrame(var_results)
df_var_report.to_csv("var_cvar_report.csv", index=False)
print("🏁 Task 1 Complete: var_cvar_report.csv generated.")

# TASK 2: ROLLING 90-DAY SHARPE RATIO
key_funds = ["Fund_1", "Fund_2", "Fund_3", "Fund_4", "Fund_5"]
df_rolling_sharpe = pd.DataFrame(index=df_returns.index)
for fund in key_funds:
    rolling_mean = df_returns[fund].rolling(90).mean()
    rolling_std = df_returns[fund].rolling(90).std()
    df_rolling_sharpe[fund] = (rolling_mean / rolling_std) * np.sqrt(252)

plt.figure(figsize=(10, 5))
for fund in key_funds:
    plt.plot(df_rolling_sharpe.index, df_rolling_sharpe[fund], label=fund)
plt.title("90-Day Rolling Sharpe Ratio Evolution")
plt.xlabel("Date")
plt.ylabel("Annualized Sharpe Ratio")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.savefig("rolling_sharpe_chart.png", dpi=300)
plt.close()
print("🏁 Task 2 Complete: rolling_sharpe_chart.png saved.")

# TASK 3: INVESTOR COHORT ANALYSIS
investor_records = pd.DataFrame({
    "Investor_ID": range(1001, 2001),
    "First_Tx_Year": np.random.choice([2022, 2023, 2024, 2025], 1000),
    "Avg_SIP_Amount": np.random.uniform(2000, 25000, 1000),
    "Total_Invested": np.random.uniform(50000, 1000000, 1000),
    "Preferred_Fund": np.random.choice(funds, 1000)
})
cohort_analysis = investor_records.groupby("First_Tx_Year").agg(
    Avg_SIP=("Avg_SIP_Amount", "mean"),
    Total_Capital=("Total_Invested", "sum"),
    Top_Fund_Preference=("Preferred_Fund", lambda x: x.mode()[0])
).reset_index()
print("\n--- TASK 3: INVESTOR COHORT REPORT ---")
print(cohort_analysis.to_string(index=False))

# TASK 4: SIP CONTINUITY ANALYSIS
tx_data = []
for inv_id in range(1001, 1150):
    num_tx = np.random.randint(6, 12)
    base_dates = pd.date_range(start="2025-01-01", periods=num_tx, freq="30D")
    random_noise = np.random.randint(-5, 12, size=num_tx)
    adjusted_dates = [base_dates[i] + pd.Timedelta(days=int(random_noise[i])) for i in range(num_tx)]
    for dt in adjusted_dates:
        tx_data.append({"Investor_ID": inv_id, "Tx_Date": dt})

df_tx = pd.DataFrame(tx_data).sort_values(by=["Investor_ID", "Tx_Date"])
risk_profiles = []
for inv_id, group in df_tx.groupby("Investor_ID"):
    gaps = group["Tx_Date"].diff().dt.days.dropna()
    avg_gap = gaps.mean()
    status = "at-risk" if (gaps > 35).any() else "active"
    risk_profiles.append({"Investor_ID": inv_id, "Avg_Gap_Days": avg_gap, "Status": status})
df_retention = pd.DataFrame(risk_profiles)
print(f"🏁 Task 4 Complete: Flagged {len(df_retention[df_retention['Status']=='at-risk'])} accounts as 'at-risk'.")

# TASK 6: PORTFOLIO SECTOR HHI CONCENTRATION
sector_weights = np.random.dirichlet(np.ones(6), size=40)
hhi_scores = []
for i, fund in enumerate(funds):
    weights = sector_weights[i]
    hhi = np.sum((weights * 100) ** 2)
    hhi_scores.append({"Fund_Name": fund, "HHI": hhi})
df_hhi = pd.DataFrame(hhi_scores)
print(f"🏁 Task 6 Complete: Maximum asset concentration evaluated at HHI: {df_hhi['HHI'].max():.2f}")