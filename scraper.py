import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException, TimeoutException, WebDriverException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # Import By from selenium.webdriver.common
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging at the start
logging.basicConfig(level=logging.INFO)
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/teradakousuke/Library/Mobile Documents/com~apple~CloudDocs/Scriping tool/credentials.json', scope)
gc = gspread.authorize(creds)

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Install ChromeDriver
chrome_service = Service(ChromeDriverManager().install())

# Initialize WebDriver once using the installed ChromeDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Set up wait
wait = WebDriverWait(driver, 10)  # 10 seconds timeout

# Access the top page
driver.get('https://works.litalico.jp/center/')

# Get links to each region's page using JavaScript
region_links = []
for i in range(1, 8):  # As li:nth-child goes up to 7
    for j in range(1, 7):  # As li:nth-child goes up to 6
        selector = f'#sidebar_localNav > ul > li:nth-child({i}) > ul > li:nth-child({j}) > a'
        # Execute JavaScript to find the element
        element = driver.execute_script(f"return document.querySelector('{selector}')")
        if element:
            region_links.append(element.get_attribute('href'))
        else:
            break  # Stop the inner loop if no element is found for the current index

# Use the previously authenticated client
try:
    wb = gc.open("AllCentersData")
except gspread.SpreadsheetNotFound:
    wb = gc.create("AllCentersData")

worksheet = wb.get_worksheet(0)

# Add a header row if needed
if worksheet.row_count == 0:
    worksheet.append_row(['事業所名', 'アクセス', '住所', '電話番号'])

all_rows = []  # List to hold all rows of data


# Extract data from each region's page
for region_link in region_links:
    try:
        driver.get(region_link)
        # Wait for the page to fully load
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        # Now retrieve the center ids using JavaScript
        js_script = '''
            var elements = document.querySelectorAll('.centerList .centerElement');
            var ids = [];
            for(var i = 0; i < elements.length; i++) {
                ids.push(elements[i].getAttribute('id'));
            }
            return ids;
        '''
        center_ids = driver.execute_script(js_script)
        
        for center_id in center_ids:
            try:
                # Data extraction code block
                element1_link_element = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f'#{center_id} > div.p-center__centerlist-header > a')))
                element1_link = element1_link_element.get_attribute('href')
                element1_name = element1_link_element.find_element(By.CSS_SELECTOR, 'h2 > span.p-center__centerlist-name').text
                
                element2 = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f'#{center_id} > div.p-center__centerlist-body > div.p-center__centerlist-body-detail > div.p-center__centerlist-info > div:nth-child(1) > div'))).text
                
                element3 = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f'#{center_id} > div.p-center__centerlist-body > div.p-center__centerlist-body-detail > div.p-center__centerlist-info > div:nth-child(2) > div'))).text
                
                element4_tel = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f'#{center_id} > div.p-center__centerlist-body > div.p-center__centerlist-body-detail > div.p-center__centerlist-info > div:nth-child(3) > div > a'))).get_attribute('href').replace('tel:', '')
                
                # Append the data to the all_rows list
                all_rows.append([element1_name, element2, element3, element4_tel])

            except NoSuchElementException as e:
                logging.error(f"Failed to find an element for center ID {center_id}: {e}")
            except TimeoutException as e:
                logging.error(f"Timeout while waiting for an element for center ID {center_id}: {e}")
            # End of data extraction code block
            
    except WebDriverException as e:
        logging.error(f"Web driver error occurred while processing region link {region_link}: {e}")

# Append all rows to the worksheet in one batch
if all_rows:
    worksheet.append_rows(all_rows)

# Close WebDriver
driver.quit()
