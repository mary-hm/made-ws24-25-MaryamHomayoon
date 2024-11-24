import re
import pandas as pd
import sqlite3
import requests
from io import BytesIO

# SQLite database paths
db1_path = './data/educational_attainment.sqlite'
db2_path = './data/unemployed_data.sqlite'

# Function to fetch files from a URL
def fetch_file_to_memory(file_url):
    """Fetch a file from a URL and load it into memory."""
    response = requests.get(file_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch file from URL: {file_url}")
    return BytesIO(response.content)

# Function to clean and transform the educational attainment dataset
def process_education(file_urls):
    """Process and clean the educational attainment datasets."""
    all_combined_data = []

    def extract_year_from_text(data):
        """Extract the year from descriptive text."""
        for row in data.iloc[:10, 0]:  # Focus on the first column where metadata is likely stored
            if isinstance(row, str):
                match = re.search(r'\b(20\d{2})\b', row)  # Look for a year pattern like '2022'
                if match:
                    return int(match.group(1))
        raise ValueError("Year not found in file")

    for url in file_urls:
        file_obj = fetch_file_to_memory(url)
        raw_data = pd.read_excel(file_obj, sheet_name=0, header=None)

        # Extract year
        year = extract_year_from_text(raw_data)

        # Process data
        data = pd.read_excel(file_obj, sheet_name=0, skiprows=5, header=0)
        data.columns = [col.strip().replace('3', '').replace('2', '') for col in data.columns]
        
        # Extract "Both Sexes" data
        start_idx = data[data['Unnamed: 0'] == 'Both Sexes'].index[0]
        try:
            end_idx = data[(data['Unnamed: 0'] == 'Male') | (data['Unnamed: 0'] == 'Female')].index[0]
        except IndexError:
            end_idx = len(data)

        both_sexes_data = data.iloc[start_idx+1:end_idx]
        both_sexes_data = both_sexes_data[~both_sexes_data['Unnamed: 0'].str.contains("18 years and over|25 years and over|Male|Female", na=False)]
        both_sexes_data = both_sexes_data.dropna(subset=['Unnamed: 0'])
        both_sexes_data['Year'] = year

        all_combined_data.append(both_sexes_data)

    # Combine all data
    combined_data = pd.concat(all_combined_data, ignore_index=True)

    # Save to SQLite
    conn = sqlite3.connect(db1_path)
    combined_data.to_sql("educational_attainment", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Educational attainment data saved to '{db1_path}'.")

# Function to clean and transform the unemployment dataset
def process_unemployment(file_url):
    """Clean and transform the dataset."""
    df = pd.read_excel(fetch_file_to_memory(file_url), skiprows=2)

    # Remove rows where the first column contains only numeric values
    df['Age group and highest level of educational attainment'] = df[
        'Age group and highest level of educational attainment'
    ].astype(str)
    df = df[
        ~df['Age group and highest level of educational attainment'].str.isdigit()
    ]

    # Remove rows starting from '--Not available' to the end of the table, including '--Not available'
    not_available_index = df[
        df['Age group and highest level of educational attainment'].str.contains('---Not available.', na=False)
    ].index.min()
    if not_available_index is not None:
        df = df.iloc[:not_available_index]

    # Consolidate columns for each year into a single column
    years = [2017, 2018, 2019, 2020, 2021, 2022]
    for year in years:
        rate_col = year
        std_error_col = f"Unnamed: {df.columns.get_loc(year) + 2}"
        df[year] = df[rate_col].astype(str) + ", " + df[std_error_col].astype(str)

    # Keep only the relevant columns
    result_df = df[['Age group and highest level of educational attainment'] + years]

    # Save to SQLite
    conn = sqlite3.connect(db2_path)
    result_df.to_sql("cleaned_table", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Unemployment dataset saved to '{db2_path}'.")

# URLs for datasets
edu_attainment_urls = [
    "https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2022/cps-detailed-tables/table-1-1.xlsx",
    "https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2021/cps-detailed-tables/table-1-1.xlsx",
    "https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2020/cps-detailed-tables/table-1-1.xlsx",
    "https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2019/cps-detailed-tables/table-1-1.xlsx",
    "https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2018/cps-detailed-tables/table-1-1.xlsx",
    "https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2017/cps-detailed-tables/table-1-1.xlsx",
]

unemployment_url = "https://nces.ed.gov/programs/digest/d22/tables/xls/tabn501.80.xlsx"

# Run both processing functions
process_education(edu_attainment_urls)
process_unemployment(unemployment_url)
