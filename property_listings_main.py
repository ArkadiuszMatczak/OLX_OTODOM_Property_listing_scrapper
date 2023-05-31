from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from web_manipulation import WebManipulation


# Create a new instance of the browser driver
driver = webdriver.Chrome()

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

def get_all_listings():
    pagecount = int(wm.get_element_text('//button[@aria-label="następna strona"]/preceding-sibling::button[1]'))
    print(pagecount)
    for page_index in range(pagecount):
        if page_index != 0:
            time.sleep(1)
            wm.scroll_to_bottom()
            #dodac scroll do elementu zanim klikniesz
            wm.click_element(f'//button[contains(@aria-label, "Idź do strony") and contains(text(), "{(page_index+1)}")]')
        time.sleep(1)
        wm.scroll_to_bottom()
        listings_count = wm.get_elements_count('//a[@data-cy="listing-item-link"]')
        print(listings_count)
        for i in range(listings_count):
            print(i)
get_all_listings()
# Close the browser
driver.quit()
