import requests
import pandas as pd
import os
import time

def fetch_and_save_schemes(scheme_codes):
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🚀 Starting Extraction Loop for {len(scheme_codes)} target schemes...")
    print("=" * 60)
    
    for code in scheme_codes:
        url = f"https://api.mfapi.in/mf/{code}"
        print(f"📡 Requesting API data for Code: {code}...")
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                json_data = response.json()
                
                # Metadata identification
                meta = json_data.get('meta', {})
                scheme_name = meta.get('scheme_name', 'Unknown Scheme')
                print(f"✅ Found: {scheme_name}")
                
                # Extract time series
                nav_rows = json_data.get('data', [])
                if nav_rows:
                    df = pd.DataFrame(nav_rows)
                    
                    # Target delivery path
                    output_file = f"{output_dir}/nav_history_{code}.csv"
                    df.to_csv(output_file, index=False)
                    print(f"📦 Saved {len(df)} rows to {output_file}")
                else:
                    print(f"⚠️ No data rows found for code {code}")
            else:
                print(f"❌ API Error for code {code}. Status Code: {response.status_code}")
                
        except Exception as e:
            print(f"💥 Failed to execute stream loop for code {code}: {e}")
            
        print("-" * 60)
        time.sleep(1) # Graceful delay between API hits

if __name__ == "__main__":
    # The explicit mandatory target codes from your Day 1 assignments
    required_targets = [
        "125497",  # HDFC Top 100 Direct (Task 4)
        "119551",  # SBI Bluechip (Task 5)
        "120503",  # ICICI Bluechip (Task 5)
        "118632",  # Nippon Large Cap (Task 5)
        "119092",  # Axis Bluechip (Task 5)
        "120841"   # Kotak Bluechip (Task 5)
    ]
    fetch_and_save_schemes(required_targets)