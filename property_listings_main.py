
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from web_manipulation import WebManipulation, GetNewListings
from selenium.webdriver.chrome.options import Options

max_price = '500000'
min_price = '505000'
min_area = '50'


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
wm.send_keys_to_element('//input[@id="priceMin"]', min_price)
# input maximum price
wm.click_element('//input[@id="priceMax"]')
wm.send_keys_to_element('//input[@id="priceMax"]', max_price)
# input minimum area
wm.click_element('//input[@id="areaMin"]')
wm.send_keys_to_element('//input[@id="areaMin"]', min_area)
# click search
wm.click_element('//button[@id="search-form-submit"]')
# interate throw all listings on each page and extract only new listings
gnl = GetNewListings(driver)
# xpaths requiered for data extraction
otodom_path = "C:/Users/lenovo/Property listings/compareData.pkl"
otodom_page_count = '//button[@aria-label="następna strona"]/preceding-sibling::button[1]'
otodom_next_page = '//button[@aria-label="następna strona"]'
otodom_listing_link = '//ul/li[@data-cy="listing-item"]/a[@data-cy="listing-item-link"]'
#
set_otodom = gnl.get_new_listings(otodom_path, otodom_page_count, otodom_next_page, otodom_listing_link)

wm.launch('https://www.olx.pl/')
wm.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')
wm.click_element('//a/span[contains(text(), "Nieruchomości")]/following-sibling::span')
wm.click_element('//span[contains(text(), "Mieszkania")]')

wm.write_into_element_with_actionchains('//input[@data-testid="location-search-input"]', 'łódź')

wm.click_element('(//input[@data-testid="range-to-input"])[1]')
wm.write_into_element_with_actionchains('(//input[@data-testid="range-to-input"])[1]', max_price)

wm.click_element('(//input[@data-testid="range-from-input"])[1]')
wm.write_into_element_with_actionchains('(//input[@data-testid="range-from-input"])[1]', min_price)

wm.click_element('(//input[@data-testid="range-from-input"])[2]')
wm.write_into_element_with_actionchains('(//input[@data-testid="range-from-input"])[2]', min_area)

wm.click_element('//button[@data-testid="search-submit"]')

gnl = GetNewListings(driver)
# xpaths requiered for data extraction
olx_path = "C:/Users/lenovo/Property listings/compareData1.pkl"
olx_page_count = '//a[@data-testid="pagination-forward"]/preceding-sibling::li[1]'
olx_next_page = '//a[@data-testid="pagination-forward"]'
olx_listing_link = '//div[@data-cy="l-card"]/a'
#
set_olx = gnl.get_new_listings(olx_path, olx_page_count, olx_next_page, olx_listing_link)

set_combine_listings = set_olx | set_otodom
print("Main listing set")
print(set_combine_listings)

# Close the connection
driver.quit()