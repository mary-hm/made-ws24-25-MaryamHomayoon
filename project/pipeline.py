import re
import pandas as pd
import sqlite3
import requests
from io import BytesIO

# SQLite database paths
db1_path = '../data/educational_attainment.sqlite'
db2_path = '../data/unemployed_data.sqlite'

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

# Function to fetch files from a URL and load it into memory
def fetch_file_to_memory(file_url):
   
    response = requests.get(file_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch file from URL: {file_url}")
    return BytesIO(response.content)

# Function to clean and transform the educational attainment dataset, Combining educational grades and ordering columns
def process_education(file_urls):
 
    all_combined_data = []

    # Extract the year from descriptive text.
    def extract_year_from_text(data):
        
        for row in data.iloc[:10, 0]:  # Focus on the first column where metadata is likely stored
            if isinstance(row, str):
                match = re.search(r'\b(20\d{2})\b', row)  # Look for a year pattern like '2022'
                if match:
                    return int(match.group(1))
        raise ValueError("Year not found in file")

    # Define age ranges to combine
    age_combinations = {
        "25 to 34 years": ["25 to 29 years", "30 to 34 years"],
        "35 to 44 years": ["35 to 39 years", "40 to 44 years"],
        "45 to 54 years": ["45 to 49 years", "50 to 54 years"],
        "55 to 64 years": ["55 to 59 years", "60 to 64 years"]
    }

    # Define age ranges to exclude
    excluded_ranges = ["65 to 69 years", "70 to 74 years", "75 years and over"]

    # Define educational grade combinations
    grade_combinations = {
        "Less than high school completion": [
            "None",
            "1st - 4th grade",
            "5th - 6th grade",
            "7th - 8th grade",
            "9th grade",
            "10th grade",
            "11th grade2"
        ],
        "Some college, no bachelor's degree": [
            "Some college, no degree",
            "Associate's degree, occupational",
            "Associate's degree, academic"
        ],
        "Bachelor's or higher degree": [
            "Bachelor's degree",
            "Master's degree",
            "Professional degree",
            "Doctoral degree"
        ]
    }

    for url in file_urls:
        file_obj = fetch_file_to_memory(url)
        raw_data = pd.read_excel(file_obj, sheet_name=0, header=None)

        # Extract year
        year = extract_year_from_text(raw_data)

        # Process data
        data = pd.read_excel(file_obj, sheet_name=0, skiprows=5, header=0)

        # Standardize column names
        standardized_columns = {
            "High school graduate3": "High school graduate"
        }
        data.columns = [standardized_columns.get(col.strip(), col.strip()) for col in data.columns]

        # Extract "Both Sexes" data
        start_idx = data[data['Unnamed: 0'] == 'Both Sexes'].index[0]
        try:
            end_idx = data[(data['Unnamed: 0'] == 'Male') | (data['Unnamed: 0'] == 'Female')].index[0]
        except IndexError:
            end_idx = len(data)

        both_sexes_data = data.iloc[start_idx + 1:end_idx]
        both_sexes_data = both_sexes_data.dropna(subset=['Unnamed: 0'])

        # Rename the 'Unnamed: 0' column to 'Age groups'
        both_sexes_data.rename(columns={'Unnamed: 0': 'Age groups'}, inplace=True)

        # Clean up the 'Age groups' column to handle formatting issues
        both_sexes_data['Age groups'] = both_sexes_data['Age groups'].str.strip().str.lstrip('.')

        # Add year column
        both_sexes_data['Year'] = year

        # Drop excluded age ranges
        both_sexes_data = both_sexes_data[~both_sexes_data['Age groups'].isin(excluded_ranges)]

        # Combine rows for the specified age ranges
        for new_label, ranges in age_combinations.items():
            age_group_rows = both_sexes_data[both_sexes_data['Age groups'].isin(ranges)]
            if not age_group_rows.empty:
                combined_row = age_group_rows.groupby('Year', as_index=False).sum(numeric_only=True)
                combined_row['Age groups'] = new_label
                both_sexes_data = both_sexes_data[~both_sexes_data['Age groups'].isin(ranges)]
                both_sexes_data = pd.concat([both_sexes_data, combined_row], ignore_index=True)

        # Combine educational grades
        for new_label, cols in grade_combinations.items():
            both_sexes_data[new_label] = both_sexes_data[cols].sum(axis=1)
            both_sexes_data.drop(columns=cols, inplace=True)

        all_combined_data.append(both_sexes_data)

    # Combine all data
    combined_data = pd.concat(all_combined_data, ignore_index=True)

    # Reorder columns
    column_order = [
        "Age groups",
        "Total",
        "Less than high school completion",
        "High school graduate",
        "Some college, no bachelor's degree",
        "Bachelor's or higher degree",
        "Year",
    ]
    combined_data = combined_data[[col for col in column_order if col in combined_data.columns]]

    # Save to SQLite
    conn = sqlite3.connect(db1_path)
    combined_data.to_sql("educational_attainment", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Educational attainment data saved to '{db1_path}'.")

# Function to Clean and transform the unemployment dataset, dropping specific age ranges and trailing empty rows
# Function to Clean and transform the unemployment dataset, dropping specific age ranges and trailing empty rows
# Includes row name cleaning as previously done in `clean_row_names`
def process_unemployment(file_url):
    df = pd.read_excel(fetch_file_to_memory(file_url), skiprows=2)

    # Remove rows where the first column contains only numeric values
    df['Age group and highest level of educational attainment'] = df[
        'Age group and highest level of educational attainment'
    ].astype(str)
    df = df[
        ~df['Age group and highest level of educational attainment'].str.isdigit()
    ]

    # Remove rows starting from '25 to 64 years old' and associated rows below until a new age group appears
    is_excluded = False
    cleaned_rows = []
    for _, row in df.iterrows():
        age_group = row['Age group and highest level of educational attainment']
        if "25 to 64 years old" in age_group:
            is_excluded = True
        elif is_excluded and "years old" in age_group:  # Detects the start of a new age group
            is_excluded = False
        
        if not is_excluded:
            cleaned_rows.append(row)

    # Convert back to DataFrame
    df = pd.DataFrame(cleaned_rows)

    # Remove trailing empty rows after the last row with meaningful data
    df = df.dropna(how='all', subset=df.columns[1:])  # Check non-index columns for all-NaN rows
    last_valid_index = df.last_valid_index()
    df = df.loc[:last_valid_index]

    # Consolidate columns for each year into a single column
    years = [2017, 2018, 2019, 2020, 2021, 2022]
    for year in years:
        rate_col = year
        std_error_col = f"Unnamed: {df.columns.get_loc(year) + 2}"
        df[year] = df[rate_col].astype(str) + ", " + df[std_error_col].astype(str)

    # Keep only the relevant columns
    df = df[['Age group and highest level of educational attainment'] + years]

    # Row name cleaning, Remove trailing '\number\' from row names
    df['Age group and highest level of educational attainment'] = (
        df['Age group and highest level of educational attainment']
        .str.replace(r"\\\d+\\", "", regex=True)  # Remove trailing "\number\"
        .str.strip()  # Remove leading/trailing spaces
    )

    # Replace "At least some college" with "Some college, no bachelor's degree"
    df['Age group and highest level of educational attainment'] = (
        df['Age group and highest level of educational attainment']
        .str.replace("At least some college", "Some college, no bachelor's degree", regex=False)
    )

    # Save to SQLite
    conn = sqlite3.connect(db2_path)
    df.to_sql("cleaned_table", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Unemployment dataset saved to '{db2_path}'.")


""" 
From here onward we are working with SQLite tables since it is not easy to do all the cleaning and transformation to the fetched data
due to its' due to its poorly structured nature
"""

# Append the respective age range to the beginning of related educational level rows,
# handling formatting inconsistencies in the specified SQLite table
def append_age_to_levels(db_path, table_name):

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f"SELECT * FROM {table_name};", conn)

    # Normalize the 'Age group and highest level of educational attainment' column
    df['Age group and highest level of educational attainment'] = (
        df['Age group and highest level of educational attainment']
        .str.strip()  # Remove leading/trailing spaces
        .str.replace(r'\s+', ' ', regex=True)  # Replace multiple spaces with one
    )

    # Propagate the age range
    current_age_range = None
    for index, row in df.iterrows():
        age_group = row['Age group and highest level of educational attainment']
        if re.match(r"^\d+\s*to\s*\d+\s*years old", age_group) and "all education" in age_group:
            # Extract just the age range (e.g., "16 to 19") using regex
            match = re.match(r"(\d+\s*to\s*\d+)", age_group)
            if match:
                current_age_range = match.group(1).strip()
        else:
            if current_age_range:
                # Prepend the current age range to the educational level
                df.at[index, 'Age group and highest level of educational attainment'] = f"{current_age_range} {age_group}"

    # Save the modified data back to the SQLite table
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print(f"Age ranges have been appended to the table '{table_name}'.")

# Adjusts the age ranges in the unemployment dataset by combining '16 to 19' and '20 to 24' into a new '18 to 24' age range
# for each education level, and removing the original '16 to 19' and '20 to 24' rows
def adjust_unemployment_age_ranges(db_path, table_name):

    # Connect to the database and load the table
    conn = sqlite3.connect(db_path)
    unemployment_df = pd.read_sql(f"SELECT * FROM {table_name};", conn)

    # Define levels and initialize a dictionary to store consolidated rows
    levels = ["all education levels", "Less than high school completion", 
              "High school completion", "Some college, no bachelor's degree", 
              "Bachelor's or higher degree"]
    consolidated_rows = {level: {"Age group and highest level of educational attainment": f"18 to 24 {level}"} for level in levels}
    
    years = [col for col in unemployment_df.columns if re.match(r'^\d{4}', col)]

    for year in years:
        year_data = unemployment_df[["Age group and highest level of educational attainment", year]]
        year_data = year_data.dropna()

        # Extract rows for 16 to 19 and 20 to 24
        age_16_19 = year_data[
            year_data["Age group and highest level of educational attainment"].str.contains("16 to 19", regex=False)
        ]
        age_20_24 = year_data[
            year_data["Age group and highest level of educational attainment"].str.contains("20 to 24", regex=False)
        ]

        # Compute proportional contribution of 18-19 from 16-19 (assume equal distribution across 4 years)
        factor_18_19 = 2 / 4  # 18-19 is half of 16-19 range

        # Process each educational level
        for level in levels:
            row_16_19 = age_16_19[
                age_16_19["Age group and highest level of educational attainment"].str.contains(level, regex=False)
            ]
            row_20_24 = age_20_24[
                age_20_24["Age group and highest level of educational attainment"].str.contains(level, regex=False)
            ]

            if not row_16_19.empty or not row_20_24.empty:
                # Handle missing data (e.g., Bachelor's or higher degree for 16 to 19)
                rate_16_19, std_16_19 = (0.0, 0.0) if row_16_19.empty else map(float, row_16_19.iloc[0][year].split(","))
                rate_20_24, std_20_24 = (0.0, 0.0) if row_20_24.empty else map(float, row_20_24.iloc[0][year].split(","))

                # Calculate 18 to 19 contribution
                rate_18_19 = rate_16_19 * factor_18_19
                std_18_19 = std_16_19 * factor_18_19  # Assuming error scales similarly

                # Combine 18-19 with 20-24
                combined_rate = rate_18_19 + rate_20_24
                combined_std = (std_18_19**2 + std_20_24**2)**0.5  # Combine standard errors

                # Store the combined rate and std for the current year
                consolidated_rows[level][year] = f"{combined_rate}, {combined_std}"

    # Convert consolidated rows into a DataFrame
    consolidated_df = pd.DataFrame(consolidated_rows.values())

    # Filter out the original 16 to 19 and 20 to 24 rows
    unemployment_df = unemployment_df[
        ~unemployment_df["Age group and highest level of educational attainment"].str.contains(
            "16 to 19|20 to 24", regex=True
        )
    ]

    # Append the consolidated rows to the remaining data
    unemployment_df = pd.concat([consolidated_df, unemployment_df], ignore_index=True)

    # Save the final table back to the database
    unemployment_df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print(f"Adjusted age ranges in table '{table_name}' and saved to '{db_path}'.")


# Run the processing functions
process_education(edu_attainment_urls)
process_unemployment(unemployment_url)
append_age_to_levels(db2_path, 'cleaned_table')
adjust_unemployment_age_ranges(db2_path, 'cleaned_table')