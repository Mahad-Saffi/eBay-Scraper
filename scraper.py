import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from variables import getUrl
import re

# Set up the Chrome driver
service = Service('C:/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Define the query and directory path
query = "shoes"
directory = f"data/{query}"
pages = 440

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Function to parse price and handle price range
def parse_price(price_text):
    price_pattern = re.compile(r"\$(\d+\.?\d*)\s*(?:to\s*\$(\d+\.?\d*))?")
    match = price_pattern.search(price_text)
    if match:
        lower_price = float(match.group(1))
        upper_price = float(match.group(2)) if match.group(2) else lower_price
        return lower_price, upper_price
    return None, None

# To classify shipping information
def classify_shipping(shipping_text):
    if "Free" in shipping_text:
        return "Free International Shipping"
    elif "estimate" in shipping_text:
        match = re.search(r'\$(\d+\.\d+)', shipping_text)
        if match:
            return f"Estimated Shipping Cost: ${match.group(1)}"
    else:
        match = re.search(r'\$(\d+\.\d+)', shipping_text)
        if match:
            return f"Fixed Shipping Cost: ${match.group(1)}"
    
    return None

# Function to save the HTML content of each page
def save_page_html(page_no, query):
    try:
        driver.get(getUrl(query=query, page_no=page_no))
        time.sleep(2)  # Consider using WebDriverWait for better reliability
        elements = driver.find_elements(By.CSS_SELECTOR, ".s-item.s-item__pl-on-bottom")
        all_elements_html = [element.get_attribute("outerHTML") for element in elements]
        full_page_html = '\n'.join(all_elements_html)
        with open(f"{directory}/page_{page_no}.html", "w", encoding="utf-8") as file:
            file.write(full_page_html)
        print(f"Page {page_no}: Fetched {len(elements)} items.")
        return len(elements)
    except Exception as e:
        print(f"Error fetching page {page_no}: {e}")
        return 0

# Function to extract data from the saved HTML files
def extract_data_from_html(pages):
    data = []
    for page_no in range(1, pages + 1):
        try:
            with open(f"{directory}/page_{page_no}.html", "r", encoding="utf-8") as file:
                page_html = file.read()
            soup = BeautifulSoup(page_html, "html.parser")
            elements = soup.select(".s-item.s-item__pl-on-bottom")
            for element in elements:
                title = element.select_one(".s-item__title").get_text(strip=True)
                price = element.select_one(".s-item__price").get_text(strip=True)
                upper_price, lower_price = parse_price(price)
                link = element.select_one(".s-item__link")['href']
                image_url = element.select_one('.s-item__image img')['src']
                condition = element.select_one('.SECONDARY_INFO').get_text(strip=True) if element.select_one('.SECONDARY_INFO') else None
                shipping = element.select_one('.s-item__shipping').get_text(strip=True) if element.select_one('.s-item__shipping') else None
                location = element.select_one('.s-item__location').get_text(strip=True) if element.select_one('.s-item__location') else None
                
                shipping = classify_shipping(shipping) if shipping else None
                
                # Check if both shipping and location are None
                if shipping is None and location is None:
                    continue

                data.append({
                    "title": title,
                    "upper_price": upper_price,
                    "lower_price": lower_price,
                    "link": link,
                    "image_url": image_url,
                    "condition": condition,
                    "shipping": shipping,
                    "location": location
                })
        except Exception as e:
            print(f"Error extracting data from page {page_no}: {e}")
    return data

# Function to save the data to CSV
def save_data_to_csv(data):
    df = pd.DataFrame(data)
    output_file = f"{directory}/data.csv"
    try:
        df.to_csv(output_file, index=False)
        print("Data saved successfully!")
    except PermissionError:
        print(f"Permission denied: Unable to write to {output_file}. Please ensure it is not open in another program.")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

# Main function to handle the scraping process
def scrape_ebay(query, pages):
    total_items = 0
    for page_no in range(1, pages + 1):
        items_fetched = save_page_html(page_no, query)
        total_items += items_fetched
    print(f"Total items fetched: {total_items}")
    
    data = extract_data_from_html(pages)
    save_data_to_csv(data)

# Run the scraper
try:
    scrape_ebay(query, pages)
finally:
    driver.quit()
