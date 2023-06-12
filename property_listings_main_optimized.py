from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from web_manipulation import WebManipulation, GetNewListings


class WebsiteAutomation:
    def __init__(self, url, city, cookies_Xpath, search_elements, listings_elements):
        self.url = url
        self.city = city
        self.cookies_Xpath = cookies_Xpath
        self.search_elements = search_elements
        self.listings_elements = listings_elements


    def extract_listings(self, gnl):
        return gnl.get_new_listings(
            self.listings_elements['path'],
            self.listings_elements['page_count_path'],
            self.listings_elements['next_page_path'],
            self.listings_elements['listing_link_path'],
        )

class Otodom(WebsiteAutomation):
    def __init__(self, url, city, region, cookies_Xpath, search_elements, listings_elements):
        super().__init__(url, city, cookies_Xpath, search_elements, listings_elements)
        self.region = region

    def search_website(self, wm, price_range, min_area):
        wm.launch(self.url)
        wm.accept_cookies(self.cookies_Xpath)
        wm.click_element(self.search_elements['location_path'])
        wm.send_keys_to_element(self.search_elements['location_input'], self.city)
        # select łódź checkbox
        wm.click_element(f'(//span[contains(text(), "{self.region}")]/preceding-sibling::span[descendant::text()[contains(., "{self.city}")]]/parent::span/parent::label/preceding-sibling::label)[1]')
        wm.click_element(self.search_elements['min_price_path'])
        wm.send_keys_to_element(self.search_elements['min_price_path'], price_range[0])
        wm.click_element(self.search_elements['max_price_path'])
        wm.send_keys_to_element(self.search_elements['max_price_path'], price_range[1])
        wm.click_element(self.search_elements['min_area_path'])
        wm.send_keys_to_element(self.search_elements['min_area_path'], min_area)
        wm.click_element(self.search_elements['submit_path'])

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(options=chrome_options)


def main():
    driver = init_driver()
    wm = WebManipulation(driver)
    gnl = GetNewListings(driver)

    websites = [
        Otodom(
            url="https://www.otodom.pl/",
            city='Łódź',
            region='łódzkie',
            cookies_Xpath='//button[@id="onetrust-accept-btn-handler"]',
            search_elements={
                'location_path': '//div[contains(text(), "Wybierz z listy lub wpisz miejscowość")]',
                'location_input': '//input[@id="location-picker-input"]',
                'min_price_path': '//input[@id="priceMin"]',
                'max_price_path': '//input[@id="priceMax"]',
                'min_area_path': '//input[@id="areaMin"]',
                'submit_path': '//button[@id="search-form-submit"]',
            },
            listings_elements={
                'path': "C:/Users/lenovo/Property listings/compareData.pkl",
                'page_count_path': '//button[@aria-label="następna strona"]/preceding-sibling::button[1]',
                'next_page_path': '//button[@aria-label="następna strona"]',
                'listing_link_path': '//ul/li[@data-cy="listing-item"]/a[@data-cy="listing-item-link"]',
            }
        ),
        # You can add more websites here in the same format
    ]

    price_range = ('500000', '550000')
    min_area = '60'
    listings = set()

    for website in websites:
        website.search_website(wm, price_range, min_area)
        listings |= website.extract_listings(gnl)

    print("Main listing set")
    print(listings)

    driver.quit()

if __name__ == "__main__":
    main()
