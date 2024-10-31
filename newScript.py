from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from bs4 import BeautifulSoup


# Configure WebDriver (specify the path to your driver if needed)
driver = webdriver.Chrome()
driver.get("https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge")

def collect_row_data(data):
    _table_data_xpath = '//*[@id="format0_disparea"]/tbody'
    page_source = driver.page_source
    table = driver.find_element(By.XPATH, _table_data_xpath)

    soup = BeautifulSoup(page_source, 'html.parser')

    # Locate the table
    table = soup.find('table')

    table_data = []

    # Extract the header
    headers = []

    headers = [header.text for header in table.find_all('th')]

    # Extract rows
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')
        if cells:  # Check if the row has data
            row_data = {headers[i]: cells[i].text for i in range(len(cells))}
            table_data.append(row_data)

    # Print the extracted table data
    print(table_data)
    # Convert the list to JSON
    json_data = json.dumps(table_data,ensure_ascii=False, indent=4)
    with open("table_data.json", "w", encoding="utf-8") as f:
        f.write(json_data)

    print("Data written to table_data.txt")

    # Print or save the JSON data
    print(json_data)
    pass
