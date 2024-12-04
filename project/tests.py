import os
import sqlite3
import pytest
import pandas as pd
from pathlib import Path

# Paths for SQLite databases
EDU_ATTAINMENT_DB = './data/educational_attainment.sqlite'
UNEMPLOYED_DATA_DB = './data/unemployed_data.sqlite'

# Test pipeline function imports
from pipeline import process_education, process_unemployment

# URLs for testing
EDU_ATTAINMENT_URLS = [
    "https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2022/cps-detailed-tables/table-1-1.xlsx",
]
UNEMPLOYMENT_URL = "https://nces.ed.gov/programs/digest/d22/tables/xls/tabn501.80.xlsx"

# Helper function to check SQLite table content
def check_table_exists(db_path, table_name):
    if not Path(db_path).exists():
        return False
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
    return table_name in tables

@pytest.fixture(scope="module")
def setup_edu_pipeline():
    # Runs education pipeline before tests
    process_education(EDU_ATTAINMENT_URLS)
    yield
    # Teardown: Delete the database
    if Path(EDU_ATTAINMENT_DB).exists():
        os.remove(EDU_ATTAINMENT_DB)

@pytest.fixture(scope="module")
def setup_unemployment_pipeline():
    # Runs unemployment pipeline before tests
    process_unemployment(UNEMPLOYMENT_URL)
    yield
    # Teardown: Delete the database
    if Path(UNEMPLOYED_DATA_DB).exists():
        os.remove(UNEMPLOYED_DATA_DB)

# Component test: Test educational attainment processed data structure 
def test_edu_data_processing(setup_edu_pipeline):
    
    assert check_table_exists(EDU_ATTAINMENT_DB, 'educational_attainment'), \
        "Educational attainment table not found."

# Component test: Test unemployment processed data structure
def test_unemployment_data_processing(setup_unemployment_pipeline):
    
    assert check_table_exists(UNEMPLOYED_DATA_DB, 'cleaned_table'), \
        "Unemployment table not found."

# Integration test: Validate SQLite outputs
def test_integration_edu_pipeline(setup_edu_pipeline):
    
    with sqlite3.connect(EDU_ATTAINMENT_DB) as conn:
        df = pd.read_sql("SELECT * FROM educational_attainment LIMIT 10;", conn)
    assert not df.empty, "Educational attainment data is empty after processing."

# Check for empty data values in unemployment data.
def test_integration_unemployment_pipeline(setup_unemployment_pipeline):
    
    with sqlite3.connect(UNEMPLOYED_DATA_DB) as conn:
        df = pd.read_sql("SELECT * FROM cleaned_table LIMIT 10;", conn)
    assert not df.empty, "Unemployment data is empty after processing."

# System test: Run the entire pipeline and validate that the output files are created by the pipeline.
def test_system_pipeline_execution():
    
    # Step 1: Remove existing files to simulate a clean environment
    if Path(EDU_ATTAINMENT_DB).exists():
        os.remove(EDU_ATTAINMENT_DB)
    if Path(UNEMPLOYED_DATA_DB).exists():
        os.remove(UNEMPLOYED_DATA_DB)
    
    # Step 2: Execute the pipeline (this step should create the output files)
    process_education(EDU_ATTAINMENT_URLS)
    process_unemployment(UNEMPLOYMENT_URL)
    
    # Step 3: Validate that the output files exist
    assert Path(EDU_ATTAINMENT_DB).exists(), "Educational attainment DB file was not created by the pipeline."
    assert Path(UNEMPLOYED_DATA_DB).exists(), "Unemployment DB file was not created by the pipeline."


# Runs pytest when the script is executed
if __name__ == "__main__": 
    pytest_args = ["-v", __file__]
    pytest.main(pytest_args)
