from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class WebManipulation:
    def __init__(self, driver):
        self.driver = driver

    def click_element(self, xpath):
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

    def write_into_element(self, xpath, text):
        try:
            # Wait for up to 10 seconds before throwing a TimeoutException
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].value = '" + str(text) + "';", element)
            driver.execute_script("var e = new KeyboardEvent('keydown', {'keyCode':13, 'which':13}); arguments[0].dispatchEvent(e);", element)
        except TimeoutException:
            print(f"TimeoutException: The element with the xpath '{xpath}' was not found within 10 seconds.")
        except NoSuchElementException:
            print(f"NoSuchElementException: The element with the xpath '{xpath}' does not exist on the page.")
        except Exception as e:
            print(f"Unexpected error occurred when trying to write into the element with the xpath '{xpath}': {str(e)}")


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
wm.write_into_element('//input[@id="location-picker-input"]', 'łódź')

# Close the browser
driver.quit()
