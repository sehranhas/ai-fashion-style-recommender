import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

csv_file_path = "maje_products.csv"
products_df = pd.read_csv(csv_file_path)

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

first_colors = []
last_image_urls = []

for index, row in products_df.iterrows():
    url = row['url'] 
    try:
        driver.get(url)
        time.sleep(3) 

        try:
            first_color_element = driver.find_element(By.CLASS_NAME, "color-name")
            first_color = first_color_element.text.strip()
        except Exception:
            first_color = "N/A" 

        try:
            image_elements = driver.find_elements(By.CSS_SELECTOR, ".pdpCarousel-container li a")
            last_image_url = image_elements[-1].get_attribute("data-hires") if image_elements else "N/A"
        except Exception:
            last_image_url = "N/A"  

        print(f"Processed URL {url}: First color - {first_color}, Last image URL - {last_image_url}")
        first_colors.append(first_color)
        last_image_urls.append(last_image_url)
    except Exception as e:
        first_colors.append("N/A")
        last_image_urls.append("N/A")
        print(f"Error processing URL {url}: {e}")

driver.quit()

products_df['first_color'] = first_colors
products_df['last_image_url'] = last_image_urls

updated_csv_file_path = "maje_products_updated.csv" 
products_df.to_csv(updated_csv_file_path, index=False)

print(f"Updated data saved to {updated_csv_file_path}")
