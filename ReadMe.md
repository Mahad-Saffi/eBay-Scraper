# eBay Scraper with PyQt Interface

## Project Overview

This project is a PyQt5-based application that scrapes data from eBay and displays it in a user-friendly graphical interface. It allows users to:

- Scrape eBay listings based on a search term or specific URL.
- Set the maximum number of items to scrape.
- View the scraping progress via a progress bar.
- Pause, resume, or stop the scraping process.
- Sort and search the scraped data using various algorithms.
- Display the scraped data in a table format.

The project makes use of web scraping libraries such as Selenium and BeautifulSoup, and the data is saved in CSV format. Sorting and searching algorithms are implemented to allow data manipulation.

## Features

- **Item Scraping**: Enter an item name or URL to scrape from eBay.
- **Scraping Controls**: Start, pause, resume, or stop scraping anytime.
- **Progress Monitoring**: See real-time updates on the progress bar.
- **Data Sorting**: Sort data using various sorting algorithms.
- **Data Searching**: Search data using different search algorithms.
- **Data Display**: Display scraped data in a table format.
- **CSV Export**: Automatically save scraped data to CSV files.

## Technologies Used

- **Python**: The core programming language used in this project.
- **PyQt5**: For building the graphical user interface.
- **Selenium**: For automating web browser interaction and scraping.
- **BeautifulSoup**: For parsing and extracting data from HTML.
- **Pandas**: For working with CSV files and data manipulation.
- **Threading**: For running the scraper in a background thread to keep the UI responsive.

## Requirements

To run this project, you need the following:

- Python 3.8 or higher
- PyQt5
- Selenium
- BeautifulSoup4
- Pandas
- A compatible web browser (e.g., Chrome) and the corresponding WebDriver

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/Mahad-Saffi/eBay-Scraper.git
    cd ebay-Scraper
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Download the [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads?authuser=0) and place it in your project directory.

4. Run the application:
    ```bash
    python Scrape.py
    ```

## Usage

1. **Start the Application**: Launch the application using the command above.
2. **Input Details**:
   - Enter the **item name** or **URL** you want to scrape.
   - Specify the maximum number of items to scrape.
3. **Start Scraping**: Click the "Start Scraping" button to begin scraping eBay listings.
4. **Pause/Resume/Stop Scraping**: Use the pause, resume, and stop buttons to control the scraping process.
5. **View Data**: Once scraping is complete, view the data in the table format or load previously saved CSV data.
6. **Sort/Search Data**: Use the sorting and searching dropdowns to manipulate the data.
7. **Export Data**: Data is automatically saved to a CSV file after scraping.

## Directory Structure
 Ebay-Scraper/  
│  
├── main.py  
├── Modules/  
│   ├── scraper_module.py  
│   ├── variables.py  
│   ├── helping_functions.py  
│   ├── Assests/  
│   │   └── icon.png  
├── Algorithms/  
│   ├── sorting_algorithms.py  
│   ├── searching_algorithms.py  
├── data/      
│   └── data.csv  
├── requirements.txt    
└── README.md   

## Example

Here's an example of how the UI looks:

![UI Example](https://github.com/user-attachments/assets/40153aea-a9bd-4394-be9b-e2243e19b8f7)

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you encounter any problems.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
