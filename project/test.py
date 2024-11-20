from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# GeckoDriver path
service = Service(executable_path="/home/maryam/miniconda3/envs/made/bin/geckodriver")


# Setup Firefox options to create a temporary profile
options = Options()
options.add_argument("-profile")
options.add_argument("/tmp/selenium-profile")  # Temporary folder

# Initialize WebDriver
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads")

# Automate interactions (e.g., selecting year, offense type, etc.)
# For example:
driver.find_element_by_id("year-select").send_keys("2023")
driver.find_element_by_id("Tables").send_keys("Offenders")
driver.find_element_by_id("download-button").click()

# Wait for download to complete
import time
time.sleep(10)  # Adjust as necessary

driver.quit()
