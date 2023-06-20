from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from web_manipulation import WebManipulation, GetNewListings


class WebsiteAutomation:
    def __init__(self, url, cookies_Xpath, search_elements, listings_elements):
        self.url = url
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
    def __init__(self, url, cookies_Xpath, search_elements, listings_elements):
        super().__init__(url, cookies_Xpath, search_elements, listings_elements)

    def search_website(self, wm, price_range, min_area, city):
        wm.launch(self.url)
        wm.accept_cookies(self.cookies_Xpath)
        wm.click_element(self.search_elements['location_path'])
        wm.send_keys_to_element(self.search_elements['location_input'], city)
        # select łódź checkbox
        # wm.click_element(f'(//span[contains(text(), "{self.region}")]/preceding-sibling::span[descendant::text()[contains(., "{self.city}")]]/parent::span/parent::label/preceding-sibling::label)[1]')
        wm.click_element('//div[@data-cy="search.form.location.dropdown.list-wrapper"]//li[1]/label[1]')
        wm.click_element(self.search_elements['min_price_path'])
        wm.send_keys_to_element(self.search_elements['min_price_path'], price_range[0])
        wm.click_element(self.search_elements['max_price_path'])
        wm.send_keys_to_element(self.search_elements['max_price_path'], price_range[1])
        wm.click_element(self.search_elements['min_area_path'])
        wm.send_keys_to_element(self.search_elements['min_area_path'], min_area)
        wm.click_element(self.search_elements['submit_path'])


class Olx(WebsiteAutomation):
    def __init__(self, url, cookies_Xpath, property_Xpath, apartments_Xpath, search_elements, listings_elements):
        super().__init__(url, cookies_Xpath, search_elements, listings_elements)
        self.property_Xpath = property_Xpath
        self.apartments_Xpath = apartments_Xpath

    def search_website(self, wm, price_range, min_area, city):
        wm.launch(self.url)
        wm.accept_cookies(self.cookies_Xpath)
        wm.click_element(self.property_Xpath)
        wm.click_element(self.apartments_Xpath)
        wm.write_into_element_with_actionchains(self.search_elements['location_input'], city)
        #(//li[@data-testid="suggestion-item" and descendant::text()[contains(., 'Łódź')]])[1]
        wm.click_element(self.search_elements['location_input'])
        wm.click_element(f'(//li[@data-testid="suggestion-item" and descendant::text()[contains(., {city})]])[1]')
        wm.click_element(self.search_elements['min_price_path'])
        wm.write_into_element_with_actionchains(self.search_elements['min_price_path'], price_range[0])
        wm.click_element(self.search_elements['max_price_path'])
        wm.write_into_element_with_actionchains(self.search_elements['max_price_path'], price_range[1])
        wm.click_element(self.search_elements['min_area_path'])
        wm.write_into_element_with_actionchains(self.search_elements['min_area_path'], min_area)
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
                            'path': "C:/temp/compareData.pkl",
                            'page_count_path': '//button[@aria-label="następna strona"]/preceding-sibling::button[1]',
                            'next_page_path': '//button[@aria-label="następna strona"]',
                            'listing_link_path': '//ul/li[@data-cy="listing-item"]/a[@data-cy="listing-item-link"]',
                            }
        ),
        Olx(
            url='https://www.olx.pl/',
            cookies_Xpath='//button[@id="onetrust-accept-btn-handler"]',
            property_Xpath='//a/span[contains(text(), "Nieruchomości")]/following-sibling::span',
            apartments_Xpath='//span[contains(text(), "Mieszkania")]',
            search_elements={
                            'location_input': '//input[@data-testid="location-search-input"]',
                            'min_price_path': '(//input[@data-testid="range-from-input"])[1]',
                            'max_price_path': '(//input[@data-testid="range-to-input"])[1]',
                            'min_area_path': '(//input[@data-testid="range-from-input"])[2]',
                            'submit_path': '//button[@data-testid="search-submit"]',
                            },
            listings_elements={
                            'path': "C:/temp/compareData1.pkl",
                            'page_count_path': '//a[@data-testid="pagination-forward"]/preceding-sibling::li[1]',
                            'next_page_path': '//a[@data-testid="pagination-forward"]',
                            'listing_link_path': '//div[@data-cy="l-card"]/a',
                            }
        )
        # You can add more websites here in the same format
    ]
    city = "Łódź"
    price_range = ('580000', '620000')
    min_area = '65'
    listings = set()

    for website in websites:
        website.search_website(wm, price_range, min_area, city)
        listings |= website.extract_listings(gnl)

    print("Main listing set")
    print(listings)

    driver.quit()


if __name__ == "__main__":
    main()
