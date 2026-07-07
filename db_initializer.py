import pandas as pd
import sqlite3
import os

def init_and_seed_db():
    print("🗄️ STARTING DATABASE INITIALIZATION & SEEDING 🗄️")
    print("=" * 65)
    
    db_path = "bluestock_mf.db"
    sql_dir = "sql"
    sql_schema_path = os.path.join(sql_dir, "schema.sql")
    processed_dir = "data/processed"
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    os.makedirs(sql_dir, exist_ok=True)
    
    schema_sql = """
    CREATE TABLE IF NOT EXISTS dim_fund (
        amfi_code INTEGER PRIMARY KEY,
        fund_name TEXT NOT NULL,
        fund_house TEXT NOT NULL,
        category TEXT NOT NULL,
        sub_category TEXT NOT NULL,
        risk_category TEXT
    );

    CREATE TABLE IF NOT EXISTS fact_nav (
        nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amfi_code INTEGER,
        date DATE NOT NULL,
        nav REAL NOT NULL,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
    );

    CREATE TABLE IF NOT EXISTS fact_transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        investor_id TEXT NOT NULL,
        transaction_date DATE NOT NULL,
        amfi_code INTEGER,
        transaction_type TEXT,
        amount_inr INTEGER,
        state TEXT,
        city TEXT,
        city_tier TEXT,
        age_group TEXT,
        gender TEXT,
        annual_income_lakh REAL,
        payment_mode TEXT,
        kyc_status TEXT,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
    );

    CREATE TABLE IF NOT EXISTS fact_aum (
        aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_house TEXT NOT NULL,
        month_year TEXT NOT NULL,
        aum_crore REAL
    );

    CREATE TABLE IF NOT EXISTS fact_sip (
        sip_id INTEGER PRIMARY KEY AUTOINCREMENT,
        month_year TEXT NOT NULL,
        sip_inflow_crore REAL
    );
    """
    
    with open(sql_schema_path, "w") as f:
        f.write(schema_sql.strip())
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    print("✅ Schema structure built cleanly.")
    
    data_mappings = {
        "clean_fund_master.csv": "dim_fund",
        "clean_nav.csv": "fact_nav",
        "clean_transactions.csv": "fact_transactions",
        "clean_aum.csv": "fact_aum",
        "clean_sip.csv": "fact_sip"
    }
    
    print("\n🚀 Pumping cleaned datasets into Star Schema tables...")
    print("-" * 50)
    
    for csv_file, table_name in data_mappings.items():
        full_csv_path = os.path.join(processed_dir, csv_file)
        
        if os.path.exists(full_csv_path):
            df = pd.read_csv(full_csv_path)
            
            if table_name == "dim_fund":
                df = df.rename(columns={'scheme_name': 'fund_name', 'risk_grade': 'risk_category'})
                df = df[['amfi_code', 'fund_name', 'fund_house', 'category', 'sub_category', 'risk_category']]
                
            elif table_name == "fact_aum":
                if 'date' in df.columns: 
                    df = df.rename(columns={'date': 'month_year'})
                aum_col = [col for col in df.columns if 'aum' in col.lower()][0]
                df = df.rename(columns={aum_col: 'aum_crore'})
                df = df[['fund_house', 'month_year', 'aum_crore']]
                
            elif table_name == "fact_sip":
                # Create a strict positional dataframe mapping index positions 0 and 1
                clean_df = pd.DataFrame()
                clean_df['month_year'] = df.iloc[:, 0]
                clean_df['sip_inflow_crore'] = df.iloc[:, 1]
                df = clean_df
                
            df.to_sql(table_name, conn, if_exists="append", index=False)
            count_check = cursor.execute(f"SELECT COUNT(*) FROM {table_name};").fetchone()[0]
            print(f"📦 Seeded {count_check} rows into table '{table_name}' from {csv_file}")
        else:
            print(f"⚠️ Warning: {csv_file} not found. Skipping.")
            
    conn.close()
    print("=" * 65)
    print("🎉 Relational database 'bluestock_mf.db' populated beautifully!")

if __name__ == "__main__":
    init_and_seed_db()