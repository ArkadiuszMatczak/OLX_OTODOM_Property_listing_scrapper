from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class WebManipulation:
    def __init__(self, driver):
        self.driver = driver

    def click_element(self, xpath: str):
        try:
            # Wait for up to 10 seconds before throwing a TimeoutException
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.click()
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
            self.driver.execute_script("arguments[0].value = '" + str(text) + "';", element)
            #driver.execute_script("var e = new KeyboardEvent('keydown', {'keyCode':13, 'which':13}); arguments[0].dispatchEvent(e);", element)
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



