import pandas as pd
import numpy as np
import os

def find_file(directory, partial_name):
    """Helper function to find a file even if prefixes vary."""
    for file in os.listdir(directory):
        if partial_name.lower() in file.lower() and file.endswith('.csv'):
            return os.path.join(directory, file)
    return None

def clean_data():
    print("🧹 Starting Day 2 Data Cleaning Pipeline...")
    print("=" * 60)
    
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)
    
    # -----------------------------------------
    # 1. CLEAN NAV HISTORY (Including Imputation)
    # -----------------------------------------
    print("🔄 Processing NAV history & filling date gaps...")
    nav_path = find_file(raw_dir, "nav_history")
    if not nav_path:
        print("❌ Error: Could not find NAV history file.")
        return
        
    nav_df = pd.read_csv(nav_path)
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.drop_duplicates(subset=['amfi_code', 'date'])
    
    filled_nav_records = []
    for amfi_code, group in nav_df.groupby('amfi_code'):
        group = group.sort_values('date').set_index('date')
        full_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
        group = group.reindex(full_range)
        group['amfi_code'] = amfi_code
        group['nav'] = group['nav'].ffill()
        group = group.reset_index().rename(columns={'index': 'date'})
        filled_nav_records.append(group)
        
    final_nav_df = pd.concat(filled_nav_records, ignore_index=True)
    final_nav_df = final_nav_df[final_nav_df['nav'] > 0]
    
    final_nav_df.to_csv(f"{processed_dir}/clean_nav.csv", index=False)
    print(f"✅ Saved clean_nav.csv ({len(final_nav_df)} rows after weekend ffill)")
    
    # -----------------------------------------
    # 2. CLEAN INVESTOR TRANSACTIONS
    # -----------------------------------------
    print("\n🔄 Processing investor transactions...")
    tx_path = find_file(raw_dir, "transaction")
    if not tx_path:
        tx_path = find_file(raw_dir, "08_")
        
    if tx_path:
        tx_df = pd.read_csv(tx_path)
        tx_df['transaction_date'] = pd.to_datetime(tx_df['transaction_date'])
        tx_df['transaction_type'] = tx_df['transaction_type'].str.strip().str.upper()
        tx_df = tx_df[tx_df['amount_inr'] > 0]
        tx_df.to_csv(f"{processed_dir}/clean_transactions.csv", index=False)
        print(f"✅ Saved clean_transactions.csv ({len(tx_df)} rows)")
    else:
        print("⚠️ Warning: Transactions file not found.")
    
    # -----------------------------------------
    # 3. TRANSFER & CLEAN REMAINING CORE TABLES
    # -----------------------------------------
    print("\n🔄 Transferring master data tables...")
    
    mappings = {
        "fund_master": "clean_fund_master.csv",
        "aum_by_fund_house": "clean_aum.csv",
        "monthly_sip": "clean_sip.csv"
    }
    
    for key, output_name in mappings.items():
        file_path = find_file(raw_dir, key)
        if file_path:
            df = pd.read_csv(file_path)
            df.to_csv(f"{processed_dir}/{output_name}", index=False)
            print(f"✅ Cleaned and copied: {output_name}")
        else:
            print(f"⚠️ Warning: Could not find file matching '{key}'")
            
    print("=" * 60)
    print("🎉 Day 2 Data Cleaning execution completely done!")

if __name__ == "__main__":
    clean_data()