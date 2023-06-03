
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from web_manipulation import WebManipulation, GetNewListings
from selenium.webdriver.chrome.options import Options




# Create a new instance of the browser driver
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=chrome_options)

# Create an instance of WebManipulation
wm = WebManipulation(driver)

# Open a OTODOM
wm.launch("https://www.otodom.pl/")

# Accept cookies popup '//button[@id="onetrust-accept-btn-handler"]'
wm.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')
# Automation logic
#OTODOM
# input łódź as a city
wm.click_element('//div[contains(text(), "Wybierz z listy lub wpisz miejscowość")]')
wm.send_keys_to_element('//input[@id="location-picker-input"]', 'łódź')
# select łódź checkbox
wm.click_element('(//span[contains(text(), "łódzkie")]/preceding-sibling::span[descendant::text()[contains(., "Łódź")]]/parent::span/parent::label/preceding-sibling::label)[1]')
# input minimum price
wm.click_element('//input[@id="priceMin"]')
wm.send_keys_to_element('//input[@id="priceMin"]', '645000')
# input maximum price
wm.click_element('//input[@id="priceMax"]')
wm.send_keys_to_element('//input[@id="priceMax"]', '650000')
# input minimum area
wm.click_element('//input[@id="areaMin"]')
wm.send_keys_to_element('//input[@id="areaMin"]', '65')
# click search
wm.click_element('//button[@id="search-form-submit"]')
# interate throw all listings on each page and extract only new listings
gnl = GetNewListings(driver)
gnl.get_new_listings_Otodom("C:/Users/lenovo/Property listings/compareData.pkl")

wm.launch('https://www.olx.pl/')
wm.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')
wm.click_element('//a/span[contains(text(), "Nieruchomości")]/following-sibling::span')
wm.click_element('//span[contains(text(), "Mieszkania")]')
# Close the connection
driver.quit()