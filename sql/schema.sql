CREATE TABLE IF NOT EXISTS dim_fund (
        amfi_code INTEGER PRIMARY KEY,
        fund_name TEXT NOT NULL,
        fund_house TEXT NOT NULL,
        category TEXT NOT NULL,
        sub_category TEXT NOT NULL,
        risk_category TEXT
    );

    CREATE TABLE IF NOT EXISTS dim_date (
        date DATE PRIMARY KEY,
        year INTEGER,
        month INTEGER,
        month_name TEXT,
        day INTEGER,
        day_of_week TEXT,
        is_weekend INTEGER
    );

    CREATE TABLE IF NOT EXISTS fact_nav (
        nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amfi_code INTEGER,
        date DATE NOT NULL,
        nav REAL NOT NULL,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
        FOREIGN KEY (date) REFERENCES dim_date(date)
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
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
        FOREIGN KEY (transaction_date) REFERENCES dim_date(date)
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

    CREATE TABLE IF NOT EXISTS fact_performance (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amfi_code INTEGER,
        return_1y REAL,
        return_3y REAL,
        return_5y REAL,
        expense_ratio REAL,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
    );