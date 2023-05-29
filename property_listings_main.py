from selenium import webdriver
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

# Set the value using JavaScript
wm.click_element('//div[contains(text(), "Wybierz z listy lub wpisz miejscowość")]')
wm.send_keys_to_element('//input[@id="location-picker-input"]', 'łódź')
wm.click_element('(//span[contains(text(), "łódzkie")]/preceding-sibling::span[descendant::text()[contains(., "Łódź")]]/parent::span/parent::label/preceding-sibling::input)[1]')
# Close the browser
driver.quit()
