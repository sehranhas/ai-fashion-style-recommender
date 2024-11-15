import time
import os
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.aritzia.com/us/en/clothing?lastViewed=1")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-tile")))

os.makedirs("aritzia_images", exist_ok=True)
output_file = "aritzia_product_data.csv"

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Type", "Color", "Image_URL"])

    last_viewed_count = 0
    max_last_viewed = 3000

    while last_viewed_count < max_last_viewed:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        products_loaded = driver.find_elements(By.CLASS_NAME, "product-tile")
        last_viewed_count = len(products_loaded)
        print(f"Products viewed: {last_viewed_count}")

        if last_viewed_count >= max_last_viewed:
            print(f"Reached lastViewed={last_viewed_count}, stopping script.")
            break

        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.js-load-more__button a"))
            )
            ActionChains(driver).move_to_element(show_more_button).click().perform()
            time.sleep(2)
        except Exception as e:
            print(f"No 'Show More' button found or error: {e}")
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', class_="product-tile")

    for product in products:
        try:
            master_data = json.loads(product.get("data-master", "{}"))
            name = master_data.get("name", "Unknown")
            product_type = name.split()[-1]

            color_swatch_list = product.find('ul', class_="ar-swatches")
            if color_swatch_list:
                first_color_swatch = color_swatch_list.find('li', class_="ar-swatches__swatch-container")
                color = first_color_swatch.find('span', class_="ar-swatches__swatch").get("data-color", "Unknown")
            else:
                color = "Unknown"

            image_wrapper = product.find('div', class_="product-image")
            image_tag = image_wrapper.find('img')
            second_image_url = image_tag.get("data-mouseover-img") 
            
            writer.writerow([name, product_type, color, second_image_url])
            print(f"Saved: {name} - {color}")
        except Exception as e:
            print(f"Error processing product: {e}")

driver.quit()

df = pd.read_csv(output_file)
df.to_csv(output_file, index=False)
print("Data collection complete.")
