from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

from bs4 import BeautifulSoup
import time
import json

# Configure WebDriver (specify the path to your driver if needed)
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Optional, run in headless mode
# chrome_options.add_argument("--headless")  # Op
# driver = webdriver.Chrome(options=chrome_options)
chrome_options.add_argument("start-maximized")
driver = uc.Chrome(options=chrome_options)


def collect_row_data(data, count):
    _table_data_xpath = '//*[@id="format0_disparea"]/tbody'
    page_source = driver.page_source
    table = driver.find_element(By.XPATH, _table_data_xpath)


    table_data = []

    # Extract the header
    headers = []
    th = table.find_elements(By.TAG_NAME, "th")

    for th in table.find_elements(By.TAG_NAME, "th"):
            headers.append(th.text)

    td = table.find_elements(By.TAG_NAME, "td")
    
    state = 0
    magic_flag = 0
    for row in table.find_elements(By.TAG_NAME, "tr"):

        magic_flag+=1
        if magic_flag == 2:
            continue
        cells = row.find_elements(By.TAG_NAME, "td")


        if cells:  # Only process rows with data
            row_data = {}
            text = ""
            for i, cell in enumerate(cells):
                text += cell.text  # Map header to cell text

            row_data[headers[state]] = text
            table_data.append(row_data)
            state +=1

    data[str(count)] = table_data


    # Print or save the JSON data
    pass

def wait_for_element(xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def force_click_new_tab(link, data,count):
    # link = driver.find_element(By.XPATH, xpath)  # Update with actual link text or selector

    # Open the link in a new tab by holding down CTRL (or Command on macOS) while clicking
    ActionChains(driver).key_down(Keys.COMMAND).click(link).key_up(Keys.COMMAND).perform()

    # Wait for the new tab to open
    time.sleep(1)
    if len(driver.window_handles) == 1:
        return 0

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[1])

    # Crawl data from the new tab
    # Example: Get the page title and print it
    print("Title of new tab:", driver.title)

    # TODO
    collect_row_data(data, count)

    # Example: Find an element and print its text
    data_element = driver.find_element(By.TAG_NAME, "h1")  # Replace with actual selector
    print("Data from new tab:", data_element.text)

    # Close the new tab if desired
    driver.close()

    # Switch back to the original tab
    driver.switch_to.window(driver.window_handles[0])

try:
    # Open the target URL
    driver.get("https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge")
    row_prime = 0
    # Let the page load
    time.sleep(1)
    data = {}
    keyword_search1 = 'AQUACULTURE'
    keyword_search2 = 'viet'

    # all xpath interation
    
    advance_search_xpath = '#bodyid > div.etds_mainbd > table > tbody > tr:nth-child(1) > td.etds_mainct > table > tbody > tr:nth-child(5) > td > div > table > tbody > tr > td:nth-child(3) > a:nth-child(2)'
    input_query_search_1 = '//*[@id="ysearchinput0"]'
    input_query_search_2 = '//*[@id="ysearchinput1"]'
    checkbox_query_search_2 = '//*[@id="AddRow1"]/table/tbody/tr/td[2]/select'
    search_xpath = '//*[@id="gs32search"]'
    table_row_xpath = '//*[@id="tablefmt1"]/tbody'

    # button_a = '//*[@id="tablefmt1"]/tbody/tr[2]/td[3]/div/div[1]/table/tbody/tr[2]/td/a'
    # button_b = '//*[@id="tablefmt1"]/tbody/tr[3]/td[3]/div/div[1]/table/tbody/tr[2]/td/a'
    # button_c = '//*[@id="tablefmt1"]/tbody/tr[4]/td[3]/div/div[1]/table/tbody/tr[2]/td/a'
    # wait_for_element(advance_search_xpath)
    # handle input
    a =input()
    advance_search_button = driver.find_element(By.CSS_SELECTOR, advance_search_xpath)
    
    advance_search_button.click()



    # Fill input search
    keyword_search1_field = driver.find_element(By.XPATH, input_query_search_1)
    keyword_search2_field = driver.find_element(By.XPATH, input_query_search_2)
    keyword_search1_field.send_keys(keyword_search1)
    keyword_search2_field.send_keys(keyword_search2)
    checkbox_query_search_2_button = driver.find_element(By.XPATH, checkbox_query_search_2)
    checkbox_query_search_2_button.click()

    search_button = driver.find_element(By.XPATH, search_xpath)
    search_button.click()

    # Infinite loop to keep clicking "Next" until no more pages
    while True:
        # Find all rows in the current page (you may need to adjust the row selector based on page structure)

        # Collect all row data
        rows = driver.find_elements(By.XPATH,table_row_xpath)


        # Process each row
        for row in rows:
            columns = row.find_elements(By.CLASS_NAME, 'std2')
            # row_data = [col.text for col in columns]
            for i in columns[::8]:
                force_click_new_tab(i,data, row_prime)
                row_prime+=1


            # Print row data or save it to a list or file
        # a = input()
        # Look for the "Next" button
            # Convert the list to JSON

        # json_data = json.dumps(data,ensure_ascii=False, indent=4)
        # with open("table_data2.json", "a", encoding="utf-8") as f:
        #     f.write(json_data)

        print("Data written to table_data.txt")
        try:
            next_xpath = '//*[@id="bodyid"]/form/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/div[1]/table/tbody/tr[4]/td/div/table/tbody/tr/td[5]/table/tbody/tr/td[3]/input'
            next_button = driver.find_element(By.XPATH, next_xpath)  # Adjust text if necessary
            ActionChains(driver).move_to_element(next_button).click().perform()  # Click "Next"
            time.sleep(1)  # Wait for new page to load
        except Exception as e:
            print("No more pages or next button not found:", e)
            json_data = json.dumps(data,ensure_ascii=False, indent=4)
            with open("table_data2.json", "a", encoding="utf-8") as f:
                f.write(json_data)
            break  # Exit the loop if "Next" button is not found or other end condition is met

finally:
    # Close the driver
    driver.quit()
