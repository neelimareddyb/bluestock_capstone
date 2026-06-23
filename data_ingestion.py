import pandas as pd

def verify_raw_data():
    file_path = "data/raw/nav_history_100049.csv"
    
    print(f"Reading file from {file_path}...")
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)
    
    print("\n--- Data Frame Summary ---")
    print(f"Total Rows: {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")
    print(f"Column Names: {list(df.columns)}")
    
    print("\n--- First 5 Rows of the Dataset ---")
    print(df.head())

if __name__ == "__main__":
    verify_raw_data()