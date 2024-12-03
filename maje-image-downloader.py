import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PIL import Image
import io
import os
import re

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

input_csv = "maje_products_updated.csv" 
output_folder = "maje_images"
os.makedirs(output_folder, exist_ok=True)

def sanitize_filename(filename):
    filename = re.sub(r'[^\w\s-]', '_', filename)
    filename = re.sub(r'[/\\]', '_', filename)
    return filename

with open(input_csv, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        last_image_url = row["last_image_url"]
        name = row["name"]
        color = row["first_color"]

        try:
            response = requests.get(last_image_url, stream=True)
            if response.status_code == 200:
                safe_name = sanitize_filename(name)
                safe_color = sanitize_filename(color)
                output_path = f"{output_folder}/{safe_name}_{safe_color}.jpg"

                with open(output_path, 'wb') as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)

                print(f"Image saved for {name} - {color}")
            else:
                print(f"Failed to fetch image for {name} - {color}: {response.status_code}")

        except Exception as e:
            print(f"Error downloading image for {name}: {e}")

driver.quit()
