# Bluestock Mutual Fund Analytics Platform - Data Dictionary

[cite_start]This document provides a comprehensive column, type, and structural reference mapping for the tables deployed inside `bluestock_mf.db`[cite: 42, 155].

## 1. Dimension Table: `dim_fund`
[cite_start]Stores metadata records for all tracked asset schemes managed across Top AMCs[cite: 29, 59].
* [cite_start]**Primary Key:** `amfi_code` [cite: 127]

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY | [cite_start]Unique Association Code issued by AMFI India[cite: 127, 206]. |
| `fund_name` | TEXT | NOT NULL | [cite_start]Full operational commercial scheme naming label[cite: 206]. |
| `fund_house` | TEXT | NOT NULL | [cite_start]Asset Management Company (AMC) brand title[cite: 206]. |
| `category` | TEXT | NOT NULL | [cite_start]Asset classification tier (e.g., Equity, Debt, Hybrid)[cite: 206]. |
| `sub_category`| TEXT | NOT NULL | [cite_start]Functional capitalization structure focus (e.g., Large Cap)[cite: 206]. |
| `risk_category`| TEXT | ALLOW NULL | [cite_start]SEBI standard risk profile grade[cite: 206]. |

## 2. Fact Table: `fact_nav`
[cite_start]Stores chronological daily Net Asset Value tracking indexes for historical trendlines[cite: 62].
* **Primary Key:** Auto-incrementing `nav_id`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `nav_id` | INTEGER | PRIMARY KEY | Unique index row record sequence tracker. |
| `amfi_code` | INTEGER | FOREIGN KEY | [cite_start]Maps back to schema records in `dim_fund`[cite: 129]. |
| `date` | DATE | NOT NULL | [cite_start]Market validation calendar business day date[cite: 129, 207]. |
| `nav` | REAL | NOT NULL | [cite_start]Calculated daily valuation closure pricing metrics[cite: 129, 207]. |

## 3. Fact Table: `fact_transactions`
[cite_start]Tracks financial investment activities, order flow patterns, and investor attributes[cite: 82].
* **Primary Key:** Auto-incrementing `transaction_id`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `transaction_id` | INTEGER | PRIMARY KEY | Unique transactional tracking index sequence number. |
| `investor_id` | TEXT | NOT NULL | [cite_start]Masked unique client wallet folio account string[cite: 212]. |
| `transaction_date`| DATE | NOT NULL | [cite_start]Transaction capture timestamp calendar date[cite: 212]. |
| `amfi_code` | INTEGER | FOREIGN KEY | [cite_start]Operational destination asset scheme code reference[cite: 213]. |
| `transaction_type`| TEXT | ALLOW NULL | [cite_start]Action signature identifier: SIP / Lumpsum / Redemption[cite: 213]. |
| `amount_inr` | INTEGER | ALLOW NULL | [cite_start]Realized gross transaction value measured in INR[cite: 213]. |
| `state` | TEXT | ALLOW NULL | [cite_start]Geographic tracking location state context field[cite: 213]. |
| `city` | TEXT | ALLOW NULL | [cite_start]Geographic tracking location city category reference[cite: 213]. |
| `city_tier` | TEXT | ALLOW NULL | [cite_start]Strategic categorization tier metric (e.g., T30, B30)[cite: 213]. |
| `age_group` | TEXT | ALLOW NULL | [cite_start]Demographic age profile mapping bucket[cite: 213]. |
| `gender` | TEXT | ALLOW NULL | [cite_start]Demographic identity classification profile tracking[cite: 213]. |
| `annual_income_lakh`| REAL | ALLOW NULL | [cite_start]Documented user annual economic baseline matrix profile[cite: 213, 214]. |
| `payment_mode` | TEXT | ALLOW NULL | [cite_start]Settlement channel architecture token (e.g., UPI, Mandate)[cite: 214]. |
| `kyc_status` | TEXT | ALLOW NULL | [cite_start]Current verification compliance lifecycle processing status[cite: 214]. |

## 4. Fact Table: `fact_aum`
[cite_start]Stores quarterly macroscopic Asset Under Management indices monitored per fund house[cite: 30, 65].
* **Primary Key:** Auto-incrementing `aum_id`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `aum_id` | INTEGER | PRIMARY KEY | Unique structural chronological log identifier. |
| `fund_house` | TEXT | NOT NULL | [cite_start]Parent AMC organization brand corporate target[cite: 129]. |
| `month_year` | TEXT | NOT NULL | [cite_start]Logged reporting date cycle sequence index[cite: 129]. |
| `aum_crore` | REAL | ALLOW NULL | [cite_start]Aggregated total value volume metrics scaled in Crore INR[cite: 129]. |

## 5. Fact Table: `fact_sip`
[cite_start]Tracks industry-wide performance benchmarks for systemic SIP capital inflow changes[cite: 68].
* **Primary Key:** Auto-incrementing `sip_id`

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `sip_id` | INTEGER | PRIMARY KEY | Unique industrial trend row identifier. |
| `month_year` | TEXT | NOT NULL | [cite_start]Macro tracking month validation period anchor (YYYY-MM)[cite: 208]. |
| `sip_inflow_crore` | REAL | ALLOW NULL | [cite_start]Absolute overall monthly inflow amount measured in Crore[cite: 208, 209]. |