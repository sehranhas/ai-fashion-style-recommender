import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox') 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://us.maje.com/en/categories/view-all-clothing/?start=0&sz=332"
driver.get(url)
time.sleep(5) 

product_tiles = driver.find_elements(By.CLASS_NAME, "main-product-tile")

products = []
for tile in product_tiles:
    try:
        name_element = tile.find_element(By.CLASS_NAME, "link")
        product_name = name_element.text

        link_element = tile.find_element(By.CSS_SELECTOR, ".js-tile-anchor")
        product_url = link_element.get_attribute("href")

        product_type = product_name.split()[-1].lower()

        products.append({
            "name": product_name,
            "url": product_url,
            "type": product_type
        })
    except Exception as e:
        print(f"Error extracting product: {e}")

csv_file = "maje_products.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "url", "type"])
    writer.writeheader() 
    writer.writerows(products) 

print(f"Data saved to {csv_file}")

driver.quit()
