import requests
import pandas as pd
import os

def fetch_historical_nav(scheme_code):
    print(f"Fetching full historical layout for Scheme Code: {scheme_code}...")
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            
            # Extract basic metadata
            meta = json_data.get('meta', {})
            fund_house = meta.get('fund_house', 'Unknown')
            scheme_name = meta.get('scheme_name', 'Unknown')
            
            print(f"Target Acquired: {scheme_name} ({fund_house})")
            
            # Extract actual time-series NAV rows
            nav_rows = json_data.get('data', [])
            if not nav_rows:
                print("No historical records found for this scheme.")
                return
                
            # Convert raw rows directly into a structured Pandas DataFrame
            df = pd.DataFrame(nav_rows)
            print(f"Extracted {len(df)} structural rows of historical data.")
            
            # Ensure our output paths match the mandatory folder structure
            output_dir = "data/raw"
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = f"{output_dir}/nav_history_{scheme_code}.csv"
            df.to_csv(output_file, index=False)
            print(f"📦 System Success! File cleanly saved to: {output_file}")
            
        else:
            print(f"API Error. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Critical execution failure: {e}")

if __name__ == "__main__":
    # Let's target a major standard code (100049 is an example of an open equity fund)
    target_scheme = "100049" 
    fetch_historical_nav(target_scheme)