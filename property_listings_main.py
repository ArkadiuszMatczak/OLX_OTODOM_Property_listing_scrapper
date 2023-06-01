import pickle
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from web_manipulation import WebManipulation
from selenium.webdriver.chrome.options import Options

is_first_run = True

# Create a new instance of the browser driver
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=chrome_options)

# Open a webpage
driver.get("https://www.otodom.pl/")
driver.maximize_window()

# Interact with elements on the webpage
try:
    # Wait for up to 10 seconds before throwing a TimeoutException, Cookies pop up
    element_popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))
    )
    element_popup.click()
except TimeoutException:
    pass

# Create an instance of WebManipulation
wm = WebManipulation(driver)

# Automation logic
wm.click_element('//div[contains(text(), "Wybierz z listy lub wpisz miejscowość")]')
wm.send_keys_to_element('//input[@id="location-picker-input"]', 'łódź')
wm.click_element('(//span[contains(text(), "łódzkie")]/preceding-sibling::span[descendant::text()[contains(., "Łódź")]]/parent::span/parent::label/preceding-sibling::label)[1]')
wm.click_element('//input[@id="priceMin"]')
wm.send_keys_to_element('//input[@id="priceMin"]', '550000')
wm.click_element('//input[@id="priceMax"]')
wm.send_keys_to_element('//input[@id="priceMax"]', '650000')
wm.click_element('//input[@id="areaMin"]')
wm.send_keys_to_element('//input[@id="areaMin"]', '65')
wm.click_element('//button[@id="search-form-submit"]')

def get_new_listings(path):
    data_set = set()
    #get number of pages with listings
    pagecount = int(wm.get_element_text('//button[@aria-label="następna strona"]/preceding-sibling::button[1]'))
    for page_index in range(pagecount):
        if page_index != 0:
            time.sleep(1)
            #wm.scroll_to_element(f'//button[contains(@aria-label, "Idź do strony") and contains(text(), "{(page_index+1)}")]')
            wm.click_element(f'//button[contains(@aria-label, "Idź do strony") and contains(text(), "{(page_index+1)}")]')
        time.sleep(1)
        wm.scroll_to_bottom()
        listings_count = wm.get_elements_count('//ul/li[@data-cy="listing-item"]/a[@data-cy="listing-item-link"]')
        print(f'total listings count...............................{listings_count}')
        for i in range(listings_count):
            url_to_listing = wm.get_element_attribute(f'(//ul/li[@data-cy="listing-item"]/a[@data-cy="listing-item-link"])[{i+1}]', 'href')
            data_set.add(url_to_listing)
        print(data_set)
        print(f'page...................................{page_index+1}')

    if is_first_run:
        with open(path, 'wb') as f:
            pickle.dump(data_set, f)
    else:
        with open(path, 'rb') as f:
            compare_data = pickle.load(f)
            new_data = data_set.difference(compare_data)
            print(new_data)

get_new_listings("C:/Users/lenovo/Property listings/compareData.pkl")
# Close the browser
driver.quit()
