import pandas as pd
import numpy as np

def run_recommender(risk_input):
    funds = [f"Fund_{i}" for i in range(1, 41)]
    np.random.seed(42)
    df_engine = pd.DataFrame({
        "Fund_Name": funds,
        "risk_grade": np.random.choice(["Low", "Moderate", "High"], 40),
        "Sharpe_Ratio": np.random.uniform(0.5, 2.8, 40)
    })
    filtered_funds = df_engine[df_engine["risk_grade"].str.upper() == risk_input.upper()]
    top_3 = filtered_funds.sort_values(by="Sharpe_Ratio", ascending=False).head(3)
    print(f"\n=== TOP 3 RECOMMENDED FUNDS FOR {risk_input.upper()} RISK APPETITE ===")
    print(top_3.to_string(index=False))

if __name__ == '__main__':
    user_risk = input("Enter Risk Appetite (Low / Moderate / High): ")
    run_recommender(user_risk)