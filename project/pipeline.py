import requests
import pandas as pd
import sqlite3
import os
from io import BytesIO

# Define the URLs of the datasets
urls = [
    "https://www.bls.gov/cps/cpsaat03.xlsx",
    "https://www.bls.gov/cps/aa2022/cpsaat03.xlsx",
    "https://www.bls.gov/cps/aa2021/cpsaat03.xlsx",
    "https://www.bls.gov/cps/aa2020/cpsaat03.xlsx"
]

# Define the headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# Connect to or create the SQLite database
database_path = "./data/datasets.db"
os.makedirs(os.path.dirname(database_path), exist_ok=True)  # Ensure the directory exists
conn = sqlite3.connect(database_path)

for i, url in enumerate(urls, start=1):
    # Download the file
    print(f"Downloading {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Read the Excel file into a DataFrame
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data)
        
        # Save the DataFrame to SQLite, naming each table uniquely by year
        table_name = f"dataset_{i}"
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Saved data from {url} to table '{table_name}' in the SQLite database.")
    else:
        print(f"Failed to download {url}. HTTP Status: {response.status_code}")

# Close the database connection
conn.close()
print("All datasets saved in SQLite database.")
