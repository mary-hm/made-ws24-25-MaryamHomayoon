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

# Helper function to check if a table exists in the database
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
    process_education(EDU_ATTAINMENT_URLS)
    yield
    if Path(EDU_ATTAINMENT_DB).exists():
        os.remove(EDU_ATTAINMENT_DB)

@pytest.fixture(scope="module")
def setup_unemployment_pipeline():
    process_unemployment(UNEMPLOYMENT_URL)
    yield
    if Path(UNEMPLOYED_DATA_DB).exists():
        os.remove(UNEMPLOYED_DATA_DB)

# Component test: Validate educational attainment table creation
def test_edu_data_processing(setup_edu_pipeline):
    assert check_table_exists(EDU_ATTAINMENT_DB, 'educational_attainment')

# Component test: Validate unemployment data table creation
def test_unemployment_data_processing(setup_unemployment_pipeline):
    assert check_table_exists(UNEMPLOYED_DATA_DB, 'cleaned_table')

# Integration test: Check data content in educational attainment
def test_integration_edu_pipeline(setup_edu_pipeline):
    with sqlite3.connect(EDU_ATTAINMENT_DB) as conn:
        df = pd.read_sql("SELECT * FROM educational_attainment LIMIT 10;", conn)
    assert not df.empty

# Integration test: Check data content in unemployment table
def test_integration_unemployment_pipeline(setup_unemployment_pipeline):
    with sqlite3.connect(UNEMPLOYED_DATA_DB) as conn:
        df = pd.read_sql("SELECT * FROM cleaned_table LIMIT 10;", conn)
    assert not df.empty

# System test: Validate pipeline execution end-to-end
def test_system_pipeline_execution():
    if Path(EDU_ATTAINMENT_DB).exists():
        os.remove(EDU_ATTAINMENT_DB)
    if Path(UNEMPLOYED_DATA_DB).exists():
        os.remove(UNEMPLOYED_DATA_DB)
    
    process_education(EDU_ATTAINMENT_URLS)
    process_unemployment(UNEMPLOYMENT_URL)
    
    assert Path(EDU_ATTAINMENT_DB).exists()
    assert Path(UNEMPLOYED_DATA_DB).exists()
