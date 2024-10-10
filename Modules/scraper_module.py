import os
import time
import threading
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal
import Modules.variables as var
import Modules.helping_functions as hf


class Scraper(QObject):
    # Define signals
    update_progress_signal = pyqtSignal(int)
    display_data_signal = pyqtSignal(list)
    update_button_signal = pyqtSignal(bool, bool, bool, bool)
    update_status_signal = pyqtSignal(str)
    
    # ````````````````````````````````INITIALIZATION````````````````````````````````````

    def __init__(self, query=var.DEFAULT_URL, max_items=var.DEFAULT_MAX_ITEMS):
        super().__init__()
        self.query = query
        self.directory = var.getDirectory(query)
        self.page_no = 1
        self.total_items = 0
        self.max_items = max_items
        self.paused = False
        self.stopped = False
        self.stop_before_scraped_items = var.STOPPING_SCRAPE_BEFORE_MIN_ITEMS
        self.lock = threading.Lock()
        self.driver = None

    def initialize_driver(self):
        service = Service('C:/chromedriver-win64/chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=800,800")  # Set a fixed window size for consistency
        self.driver = webdriver.Chrome(service=service, options=options)
        
        
        
        
        
    # ``````````````````````````````````SCRAPING````````````````````````````````````````````
    
    def initialize_directory(self):
        # Create the directory if it doesn't exist
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
    
    
    def save_page_html(self):
        try:
            self.initialize_driver()
            self.driver.get(self.query)
            # Increament the page number
            self.query = hf.increment_page_no(url=self.query)
            time.sleep(2)
            
            elements = self.driver.find_elements(By.CSS_SELECTOR, ".s-item.s-item__pl-on-bottom")
            all_elements_html = [element.get_attribute("outerHTML") for element in elements]
            full_page_html = '\n'.join(all_elements_html)
            
            with open(f"{self.directory}/page_{self.page_no}.html", "w", encoding="utf-8") as file:
                file.write(full_page_html)
            print(f"Page {self.page_no}: Fetched {len(elements)} items.")
            self.update_status_signal.emit(f"Page {self.page_no}: Fetched {len(elements)} items.")
            
            return len(elements)
        except Exception as e:
            print(f"Error fetching page {self.page_no}: {e}")
            self.update_status_signal.emit(f"Error fetching page {self.page_no}: {e}")
            return 0

    def extract_data_from_html(self, page_no):
        data = []
        try:
            with open(f"{self.directory}/page_{page_no}.html", "r", encoding="utf-8") as file:
                page_html = file.read()
            
            soup = BeautifulSoup(page_html, "html.parser")
            elements = soup.select(".s-item.s-item__pl-on-bottom")
            
            for element in elements:
                title = element.select_one(".s-item__title").get_text(strip=True)
                price = element.select_one(".s-item__price").get_text(strip=True)
                
                upper_price, lower_price = hf.parse_price(price) if isinstance(hf.parse_price(price), tuple) and all(isinstance(x, (int, float)) for x in hf.parse_price(price)) else (0, 0)
                
                link = element.select_one(".s-item__link")['href']
                image_url = element.select_one('.s-item__image img')['src']
                condition = element.select_one('.SECONDARY_INFO').get_text(strip=True) if element.select_one('.SECONDARY_INFO') else "Not Found"
                shipping = element.select_one('.s-item__shipping').get_text(strip=True) if element.select_one('.s-item__shipping') else "Not Found"
                location = element.select_one('.s-item__location').get_text(strip=True) if element.select_one('.s-item__location') else "Not Found"
                
                shipping = hf.classify_shipping(shipping) if shipping else "Not Found"
                
                if shipping == "Not Found" and location == "Not Found":
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
            self.update_status_signal.emit(f"Error extracting data from page {page_no}: {e}")
        
        return data

    def save_data_to_csv(self, data):
        output_file = f"{self.directory}/data.csv"
        df = pd.DataFrame(data)
        
        if os.path.exists(output_file):
            df.to_csv(output_file, mode='a', index=False, header=False)  # Append data without header
        else:
            df.to_csv(output_file, index=False)  # Create new file if it doesn't exist
            
        print("Data saved successfully!")
        self.update_status_signal.emit("Data saved successfully!")

    def delete_html_files(self):
        for filename in os.listdir(self.directory):
            if filename.endswith(".html"):
                os.remove(os.path.join(self.directory, filename))
                
        print("HTML files deleted.")

    def scrape(self):
        self.initialize_directory()
        
        all_data = []
        while not self.stopped and self.total_items < self.max_items:
            with self.lock:
                if self.paused:
                    time.sleep(0.1)
                    continue

            items_fetched = self.save_page_html()
            if items_fetched < self.stop_before_scraped_items:
                break

            self.total_items += items_fetched
            data = self.extract_data_from_html(self.page_no)
            all_data.extend(data)
            self.save_data_to_csv(data)

            progress_percentage = 100 if int((self.total_items / self.max_items) * 100) > 100 else int((self.total_items / self.max_items) * 100)
            self.update_progress_signal.emit(progress_percentage)

            self.page_no += 1
            
            if self.total_items >= self.max_items:
                break

        self.delete_html_files()
        self.stop()
        if self.driver:
            self.driver.quit()
        all_data = hf.concatenate_csv_files(self.directory)
        self.display_data_signal.emit(all_data)




    # ``````````````````````````````````CONTROL FUNCTIONS````````````````````````````
    
    def pause(self):
        with self.lock:
            self.paused = True
        print("Scraping paused...")
        self.update_status_signal.emit("Scraping paused...")
        self.update_button_signal.emit(False, False, True, True)

    def resume(self):
        with self.lock:
            self.paused = False
        print("Scraping resumed...")
        self.update_status_signal.emit("Scraping resumed...")
        self.update_button_signal.emit(False, True, False, True)

    def stop(self):
        with self.lock:
            if not self.stopped:
                self.stopped = True
                self.update_progress_signal.emit(0)
                print(f"Stopping scraper. Current total items: {self.total_items}")
                self.update_status_signal.emit(f"Scraping stopped || Total items Scraped: {self.total_items}")
                self.update_button_signal.emit(True, False, False, False)
                
                if self.driver:
                    self.close()
                
    def close(self):
        self.driver.quit()
