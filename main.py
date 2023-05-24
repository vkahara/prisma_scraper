from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

def scroll_to_end(driver):
    products = driver.find_elements(By.CLASS_NAME, "sc-b6ec677b-1")
    number_of_items = len(products)
    while True:
        actions = ActionChains(driver)
        actions.move_to_element(products[-1])
        actions.perform()
        time.sleep(30)
        products = driver.find_elements(By.CLASS_NAME, "sc-b6ec677b-1")
        if len(products) == number_of_items:
            break
        number_of_items = len(products)


def main():
    webdriver_service = Service('C:/Users/kaharva/Downloads/chromedriver_win32/chromedriver.exe') 
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    print("Loading page...")
    driver.get("https://www.s-kaupat.fi/tuotteet")
    time.sleep(5)
    initial_element = driver.find_element(By.XPATH, '/html/body')
    actions = ActionChains(driver)
    actions.move_to_element(initial_element)

    for _ in range(6):
        actions.send_keys(Keys.TAB)

    actions.send_keys(Keys.ENTER)
    actions.perform()
    print("Page loaded.")
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, "sc-b6ec677b-1")))
    scroll_to_end(driver)
    products = driver.find_elements(By.CLASS_NAME, "sc-b6ec677b-1")

    with open("output.txt", "w", encoding="utf-8") as f:
        for product in products:
            name = product.find_element(By.CLASS_NAME, "sc-4dcde147-0.ipMTjW").text
            price = product.find_element(By.CLASS_NAME, "sc-68088102-0.hWdKPC").text
            try:
                comp_price = product.find_element(By.CLASS_NAME, "sc-67cf5218-0.EhGdO").text
            except Exception:
                comp_price = "No comparison price available"
            f.write(f'Product Name: {name} - Price: {price} - Comparison Price: {comp_price}\n')
            time.sleep(0.2)

    driver.quit()
    

if __name__ == "__main__":
    main()
