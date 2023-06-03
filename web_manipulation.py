from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import pickle

class SeleniumDriver:
    def __init__(self, driver):
        self.driver = driver


class WebManipulation(SeleniumDriver):

    def __init__(self, driver):
        super().__init__(driver)

    def launch(self, url: str):
        self.driver.get(url)
        self.driver.maximize_window()

    def accept_cookies(self, xpath: str):
        try:
            # Wait for up to 10 seconds before throwing a TimeoutException, Cookies pop up
            element_popup = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element_popup.click()
        except TimeoutException:
            pass


    def click_element(self, xpath: str):
        try:
            # Wait for up to 10 seconds before throwing a TimeoutException
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            #element.click()
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            print(f"TimeoutException: The element with the xpath '{xpath}' was not found within 10 seconds.")
        except NoSuchElementException:
            print(f"NoSuchElementException: The element with the xpath '{xpath}' does not exist on the page.")
        except Exception as e:
            print(f"Unexpected error occurred when trying to click the element with the xpath '{xpath}': {str(e)}")

    def write_into_element(self, xpath: str, text: str):
        try:
            # Wait for up to 10 seconds before throwing a TimeoutException
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            # Set the value
            self.driver.execute_script("arguments[0].value = arguments[1];", element, text)
            # Dispatch 'input' event
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", element)
            # Dispatch 'change' event
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
        except TimeoutException:
            print(f"TimeoutException: The element with the xpath '{xpath}' was not found within 10 seconds.")
        except NoSuchElementException:
            print(f"NoSuchElementException: The element with the xpath '{xpath}' does not exist on the page.")
        except Exception as e:
            print(f"Unexpected error occurred when trying to write into the element with the xpath '{xpath}': {str(e)}")

    def send_keys_to_element(self,xpath: str, keys: str):
        try:
            # Wait for up to 10 seconds before throwing a TimeoutException
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.send_keys(keys)
        except TimeoutException:
            print(f"TimeoutException: The element with the xpath '{xpath}' was not found within 10 seconds.")
        except NoSuchElementException:
            print(f"NoSuchElementException: The element with the xpath '{xpath}' does not exist on the page.")
        except Exception as e:
            print(f"Unexpected error occurred when trying to write into the element with the xpath '{xpath}': {str(e)}")

    def check_checkbox(self, xpath):
        try:
            checkbox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))

            if not checkbox.is_selected():
                checkbox.click()

        except NoSuchElementException:
            print(f"NoSuchElementException: The element with the xpath '{xpath}' does not exist on the page.")
        except TimeoutException:
            print(f"TimeoutException: The element with the xpath '{xpath}' was not found within 10 seconds.")
        except Exception as e:
            print(f"Unexpected error occurred when trying to interact with the checkbox with the xpath '{xpath}': {str(e)}")

    def get_elements_count(self, xpath: str) -> int:
        try:
            # Wait for up to 10 seconds before throwing a TimeoutException
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

            # Find all elements matching the given xpath
            elements = self.driver.find_elements(By.XPATH, xpath)
            # Return the count of these elements
            return len(elements)
        except TimeoutException:
            print(f"TimeoutException: Elements with the xpath '{xpath}' were not found within 10 seconds.")
            return 0
        except NoSuchElementException:
            print(f"NoSuchElementException: Elements with the xpath '{xpath}' do not exist on the page.")
            return 0
        except Exception as e:
            print(f"Unexpected error occurred when trying to count the elements with the xpath '{xpath}': {str(e)}")
            return 0

    def scroll_to_bottom(self):
        try:
            # Execute the JavaScript to scroll to the bottom of the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            print(f"Unexpected error occurred when trying to scroll to the bottom of the page: {str(e)}")

    def get_element_text(self, xpath: str) ->str:
        try:
            # Wait for up to 10 seconds before throwing a TimeoutException
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element.text
        except TimeoutException:
            print(f"TimeoutException: The element with the xpath '{xpath}' was not found within 10 seconds.")
        except NoSuchElementException:
            print(f"NoSuchElementException: The element with the xpath '{xpath}' does not exist on the page.")
        except Exception as e:
            print(f"Unexpected error occurred when trying to get the text of the element with the xpath '{xpath}': {str(e)}")

    def scroll_to_element(self, xpath: str):
        try:
            # Wait for up to 10 seconds before throwing a TimeoutException
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            # Scroll to the element
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
        except TimeoutException:
            print(f"TimeoutException: The element with the xpath '{xpath}' was not found within 10 seconds.")
        except NoSuchElementException:
            print(f"NoSuchElementException: The element with the xpath '{xpath}' does not exist on the page.")
        except Exception as e:
            print(f"Unexpected error occurred when trying to scroll to the element with the xpath '{xpath}': {str(e)}")

    def get_element_attribute(self, xpath: str, attribute: str):
        try:
            # Wait for up to 10 seconds before throwing a TimeoutException
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            # Get the attribute value
            attribute_value = element.get_attribute(attribute)
            return attribute_value
        except TimeoutException:
            print(f"TimeoutException: The element with the xpath '{xpath}' was not found within 10 seconds.")
            return None
        except NoSuchElementException:
            print(f"NoSuchElementException: The element with the xpath '{xpath}' does not exist on the page.")
            return None
        except Exception as e:
            print(f"Unexpected error occurred when trying to get '{attribute}' attribute of the element with the xpath '{xpath}': {str(e)}")
            return None

class GetNewListings(SeleniumDriver):
    is_first_run = False

    def __init__(self, driver):
        super().__init__(driver)


    def get_new_listings_Otodom(self, path):

        wm = WebManipulation(self.driver)
        data_set = set()
        # get number of pages with listings
        pagecount = int(wm.get_element_text('//button[@aria-label="następna strona"]/preceding-sibling::button[1]'))
        for page_index in range(pagecount):
            if page_index != 0:
                time.sleep(1)
                #wm.scroll_to_element(f'//button[contains(@aria-label, "Idź do strony") and contains(text(), "{(page_index+1)}")]')
                wm.click_element(f'//button[contains(@aria-label, "Idź do strony") and contains(text(), "{(page_index+1)}")]')
            time.sleep(1)
            # scroll to bottom in order to load all listings
            wm.scroll_to_bottom()
            listings_count = wm.get_elements_count('//ul/li[@data-cy="listing-item"]/a[@data-cy="listing-item-link"]')
            for i in range(listings_count):
                url_to_listing = wm.get_element_attribute(f'(//ul/li[@data-cy="listing-item"]/a[@data-cy="listing-item-link"])[{i+1}]', 'href')
                data_set.add(url_to_listing)


        if self.is_first_run:
            with open(path, 'wb') as f:
                pickle.dump(data_set, f)
        else:
            with open(path, 'rb') as f:
                compare_data = pickle.load(f)
                new_data = data_set.difference(compare_data)
                print(new_data)
            with open(path, 'wb') as f:
                pickle.dump(data_set, f)






