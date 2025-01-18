from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

input_file = "ami_paris_products.csv"
output_file = "ami_paris_products_updated.csv"

options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

with open(input_file, mode="r", encoding="utf-8") as infile, open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["Second_Image_URL", "Color"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        product_url = row["URL"]
        print(f"Processing: {product_url}")
        try:
            driver.get(product_url)
            time.sleep(3) 

            second_image_url = "N/A"
            try:
                image_list_container = driver.find_element(By.CLASS_NAME, "splide__list")
                second_slide = image_list_container.find_elements(By.CLASS_NAME, "splide__slide")[1]
                second_image_url = second_slide.find_element(By.TAG_NAME, "a").get_attribute("href")
            except Exception as e:
                print(f"Second image not found: {e}")

            color = "N/A"
            try:
                color_element = driver.find_element(By.CSS_SELECTOR, ".c-color-picker.product__color-picker .u-text-black")
                color = color_element.text.strip()
            except Exception as e:
                print(f"Color not found: {e}")

            row["Second_Image_URL"] = second_image_url
            row["Color"] = color
            writer.writerow(row)

            print(f"Saved: {row['Name']} - Second Image: {second_image_url} - Color: {color}")
        except Exception as e:
            print(f"Error processing {product_url}: {e}")
            row["Second_Image_URL"] = "N/A"
            row["Color"] = "N/A"
            writer.writerow(row)

driver.quit()
print("Data update complete.")
