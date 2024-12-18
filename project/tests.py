import os
import sqlite3
import pytest
import pandas as pd
from pathlib import Path
from pipeline import process_education, process_unemployment

# Paths for SQLite databases
edu_path = './data/educational_attainment.sqlite'
upemployment_path = './data/unemployed_data.sqlite'

edu_url = [
    "https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2022/cps-detailed-tables/table-1-1.xlsx",
]
unemployment_url = "https://nces.ed.gov/programs/digest/d22/tables/xls/tabn501.80.xlsx"

def table_exists(db_path, table_name):

    if not Path(db_path).exists():
        return False
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return table_name in (row[0] for row in cursor.fetchall())


@pytest.fixture(scope="module")
def clean_up():

    yield
    for db_path in [edu_path, upemployment_path]:
        if Path(db_path).exists():
            os.remove(db_path)


def test_edu_table_creation(clean_up):
    
    process_education(edu_url)
    assert table_exists(edu_path, 'educational_attainment'), "Educational attainment table not created."


def test_unemployment_table_creation(clean_up):
    
    process_unemployment(unemployment_url)
    assert table_exists(upemployment_path, 'cleaned_table'), "Unemployment table not created."


def test_edu():
    
    process_education(edu_url)
    with sqlite3.connect(edu_path) as conn:
        df = pd.read_sql("SELECT * FROM educational_attainment LIMIT 10;", conn)
    assert not df.empty, "Educational attainment table is empty."
    expected_cols = [
        "Age groups", "Total", "Less than high school completion", 
        "High school graduate", "Some college, no bachelor's degree", 
        "Bachelor's or higher degree", "Year"
    ]
    missing_cols = [col for col in expected_cols if col not in df.columns]
    assert not missing_cols, f"Missing columns in educational attainment table: {missing_cols}"


def test_unemployment():
    
    process_unemployment(unemployment_url)
    with sqlite3.connect(upemployment_path) as conn:
        df = pd.read_sql("SELECT * FROM cleaned_table LIMIT 10;", conn)
    assert not df.empty, "Unemployment table is empty."
    year_cols = ["2017", "2018", "2019", "2020", "2021", "2022"]
    missing_years = [col for col in year_cols if col not in df.columns]
    assert not missing_years, f"Missing year columns in unemployment table: {missing_years}"
    assert "Age group and highest level of educational attainment" in df.columns, \
        "Column 'Age group and highest level of educational attainment' is missing."

# System level test
def test_pipeline_end_to_end():

    # Clean up any existing files and execute the data pipeline to make sure that the output is created by the pipeline
    if Path(edu_path).exists():
        os.remove(edu_path)
    if Path(upemployment_path).exists():
        os.remove(upemployment_path)
    process_education(edu_url)
    process_unemployment(unemployment_url)

    # Verify the output files were created
    assert Path(edu_path).exists(), "Educational attainment database file was not created."
    assert Path(upemployment_path).exists(), "Unemployment database file was not created."

    # check the contents of the output files
    with sqlite3.connect(edu_path) as conn:
        edu_df = pd.read_sql("SELECT * FROM educational_attainment LIMIT 10;", conn)
        assert not edu_df.empty, "Educational attainment table is empty."
        assert "Year" in edu_df.columns, "Column 'Year' is missing in educational attainment data."

    with sqlite3.connect(upemployment_path) as conn:
        unemp_df = pd.read_sql("SELECT * FROM cleaned_table LIMIT 10;", conn)
        assert not unemp_df.empty, "Unemployment table is empty."
        assert "2017" in unemp_df.columns, "Column '2017' is missing in unemployment data."
        assert "Age group and highest level of educational attainment" in unemp_df.columns, \
            "Column 'Age group and highest level of educational attainment' is missing."
