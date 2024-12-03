import time
import csv
import requests
from bs4 import BeautifulSoup

base_url = "https://www.amiparis.com/en-us/collections/women-new-ready-to-wear?page="

output_file = "ami_paris_products.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Type", "URL", "Image_URL"])

    for page in range(1, 9):
        print(f"Scraping page {page}...")
        url = f"{base_url}{page}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        products = soup.find_all("li", {"class": "u-col-span-1 text"})

        for product in products:
            try:
                product_name = product.find("p", class_="surtitle").get_text(strip=True)

                product_type = product_name.split()[-1]

                product_url = product.find("a", class_="c-card-product__link")["href"]
                product_url = f"https://www.amiparis.com{product_url}"

                image_tag = product.find("picture", class_="womanImg").find("img")
                image_url = image_tag["src"] if image_tag else "N/A"
                image_url = f"https:{image_url}" if image_url.startswith("//") else image_url

                writer.writerow([product_name, product_type, product_url, image_url])
                print(f"Saved: {product_name} - {product_type} - {product_url} - {image_url}")
            except Exception as e:
                print(f"Error processing product: {e}")

print("Data collection complete.")
