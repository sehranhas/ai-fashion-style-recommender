import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PIL import Image
import io
import os
import re

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

input_csv = "ami_paris_products_updated.csv"
output_folder = "ami_images"
os.makedirs(output_folder, exist_ok=True)

def sanitize_filename(filename):
    filename = re.sub(r'[^\w\s-]', '_', filename)
    filename = re.sub(r'[/\\]', '_', filename)
    return filename

with open(input_csv, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        image_url = row["Second_Image_URL"]  
        name = row.get("Name", "Unnamed")   
        color = row.get("Color", "Unknown") 

        try:
            driver.get(image_url)
            time.sleep(2)

            image_element = driver.find_element(By.TAG_NAME, 'img')
            location = image_element.location
            size = image_element.size

            screenshot = driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))

            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = top + size['height']
            cropped_image = image.crop((left, top, right, bottom))

            safe_name = sanitize_filename(name)
            safe_color = sanitize_filename(color)
            output_path = f"{output_folder}/{safe_name}_{safe_color}.jpg"
            cropped_image.save(output_path)
            print(f"Screenshot saved for {name} - {color}")

        except Exception as e:
            print(f"Error capturing screenshot for {name}: {e}")

driver.quit()
