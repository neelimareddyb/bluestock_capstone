import pandas as pd
import os

def run_data_quality_checks():
    print("📊 RUNNING DAY 1 DATA QUALITY AND MASTER METRICS REPORT 📊")
    print("=" * 65)
    
    # Load Main Datasets
    master_df = pd.read_csv("data/raw/01_fund_master.csv")
    history_df = pd.read_csv("data/raw/02_nav_history.csv")
    
    # --- TASK 6: Explore fund master ---
    print("\n[TASK 6] FUND MASTER STRUCTURAL EXPLORATION:")
    print("-" * 50)
    print(f"🏢 Unique Fund Houses ({len(master_df['fund_house'].unique())}):\n   {list(master_df['fund_house'].unique())[:5]}...")
    print(f"🗂️ Unique Categories:\n   {list(master_df['category'].unique())}")
    print(f"🏷️ Unique Sub-Categories:\n   {list(master_df['sub_category'].unique())}")
    print(f"⚠️ Unique Risk Grades:\n   {list(master_df['risk_category'].unique())}")
    
    # --- TASK 7: Validate AMFI Codes ---
    print("\n[TASK 7] AMFI CODE COHESION VALIDATION:")
    print("-" * 50)
    master_codes = set(master_df['amfi_code'].unique())
    history_codes = set(history_df['amfi_code'].unique())
    
    # Check what overlaps or matches
    matching_codes = master_codes.intersection(history_codes)
    missing_in_history = master_codes - history_codes
    
    print(f"🔢 AMFI Codes in Fund Master: {len(master_codes)}")
    print(f"🔢 AMFI Codes in Provided Nav History CSV: {len(history_codes)}")
    print(f"✅ Active Intersections/Matches: {len(matching_codes)}")
    
    if missing_in_history:
        print(f"⚠️ Anomalies Detected: {len(missing_in_history)} codes from master missing in history file.")
        print(f"🔍 Missing Codes: {list(missing_in_history)}")
    else:
        print("🎉 Clean Check! Every single master-listed AMFI code exists within nav_history.")

if __name__ == "__main__":
    run_data_quality_checks()