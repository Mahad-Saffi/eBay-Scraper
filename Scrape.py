import sys
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QProgressBar, QComboBox, QTableWidget, QTableWidgetItem, 
                             QCheckBox, QWidget, QGridLayout, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal
from scraper_module import Scraper
from sorting_alogrithms import SortingAlgorithms
import variables as var
import helping_functions as hf
import os


class ScraperUI(QMainWindow):
    # Define signals
    update_progress_signal = pyqtSignal(int)
    display_data_signal = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.Attributes = ["Title", "Upper Price", "Lower Price", "Link", "Image Url", "Condition", "Shipping", "Location"]
        self.setWindowTitle("Web Scraper")
        self.setGeometry(300, 300, 800, 800)

        # Initialize the scraper
        self.scraper = Scraper()

        # Main layout
        layout = QVBoxLayout()

        # Input for item name and URL
        self.item_label = QLabel("Enter Item Name:")
        self.item_input = QLineEdit()
        self.url_label = QLabel("Enter URL:")
        self.url_input = QLineEdit()

        layout.addWidget(self.item_label)
        layout.addWidget(self.item_input)
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        # Input for maximum number of items to scrape
        self.max_items_label = QLabel("Max Number of Items to Scrape:")
        self.max_items_input = QLineEdit()
        layout.addWidget(self.max_items_label)
        layout.addWidget(self.max_items_input)

        # Buttons for scraping control
        self.start_button = QPushButton("Start Scraping")
        self.pause_button = QPushButton("Pause Scraping")
        self.resume_button = QPushButton("Resume Scraping")
        self.stop_button = QPushButton("Stop Scraping")

        # Initially disable buttons except start
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)
        self.stop_button.setEnabled(False)

        # Add buttons to layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.resume_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        # Sorting options
        self.sort_algo_label = QLabel("Choose Sorting Algorithm:")
        self.sort_algo_dropdown = QComboBox()
        self.sort_algo_dropdown.addItems(var.SORTING_ALGORITHMS)
        self.sort_column_label = QLabel("Select Column for Sorting:")
        self.sort_column_dropdown = QComboBox()
        self.sort_column_dropdown.addItems(self.Attributes)
        layout.addWidget(self.sort_algo_label)
        layout.addWidget(self.sort_algo_dropdown)
        layout.addWidget(self.sort_column_label)
        layout.addWidget(self.sort_column_dropdown)
        self.sort_button = QPushButton("Sort Data")
        layout.addWidget(self.sort_button)

        # Searching options
        self.search_algo_label = QLabel("Choose Search Algorithm:")
        self.search_algo_dropdown = QComboBox()
        self.search_algo_dropdown.addItems(var.SEARCHING_ALGORITHMS)
        self.search_column_label = QLabel("Select Column for Searching:")
        self.search_column_dropdown = QComboBox()
        self.search_column_dropdown.addItems(self.Attributes)
        self.search_input = QLineEdit("Enter Search Term")
        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(["Contains", "Starts With", "Ends With"])
        layout.addWidget(self.search_algo_label)
        layout.addWidget(self.search_algo_dropdown)
        layout.addWidget(self.search_column_label)
        layout.addWidget(self.search_column_dropdown)
        layout.addWidget(self.search_input)
        layout.addWidget(self.filter_dropdown)
        self.search_button = QPushButton("Search Data")
        layout.addWidget(self.search_button)

        # Table to display scraped data
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Assuming 7 attributes per entity
        self.table.setHorizontalHeaderLabels(self.Attributes)
        layout.addWidget(self.table)
        self.display_data_button = QPushButton("Display Data")
        layout.addWidget(self.display_data_button)

        # Set up button actions
        self.start_button.clicked.connect(self.start_scraping)
        self.pause_button.clicked.connect(self.pause_scraping)
        self.resume_button.clicked.connect(self.resume_scraping)
        self.stop_button.clicked.connect(self.stop_scraping)
        self.sort_button.clicked.connect(self.sort_data)
        self.search_button.clicked.connect(self.search_data)
        self.display_data_button.clicked.connect(self.on_display_data_button_clicked)

        # Create central widget and set layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.update_progress_signal.connect(self.update_progress)
        self.display_data_signal.connect(self.display_data)

    def start_scraping(self):
        self.progress_bar.setValue(0)
        
        # Get the item name, URL, and max items from input fields
        item_name = self.item_input.text().replace(" ", "+")
        item_url = self.url_input.text()
        max_items = int(self.max_items_input.text()) if self.max_items_input.text().isdigit() else 25000

        if not item_name and not item_url:
            self.status_label.setText("Status: Please enter item name")
            return
        if item_name and item_url:
            self.status_label.setText("Status: Please enter either item name or URL")
            return
        if item_name and not item_url:
            self.query = var.getUrl(item_name)
        else:
            self.query = item_url

        self.scraper = Scraper(query=self.query, max_items=max_items)
        self.scraper.update_progress_signal.connect(self.update_progress_signal.emit)
        self.scraper.display_data_signal.connect(self.display_data_signal.emit)

        # Start the scraper in a separate thread using threading
        threading.Thread(target=self.run_scraper).start()

        # Update UI components
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Status: Scraping...")

    def run_scraper(self):
        self.scraper.scrape()

    def pause_scraping(self):
        if self.scraper:
            self.scraper.pause()
            self.status_label.setText("Status: Paused")
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(True)

    def resume_scraping(self):
        if self.scraper:
            self.scraper.resume()
            self.status_label.setText("Status: Resumed")
            self.resume_button.setEnabled(False)
            self.pause_button.setEnabled(True)

    def stop_scraping(self):
        if self.scraper:
            self.scraper.stop()
            self.status_label.setText("Status: Stopped")
            self.progress_bar.setValue(0)
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(False)
            self.stop_button.setEnabled(False)

    def update_progress(self, progress):
        max_items = int(self.max_items_input.text()) if self.max_items_input.text().isdigit() else 25000
        percentage = (progress / max_items) * 100
        self.progress_bar.setValue(int(percentage))
        if percentage >= 100:
            self.status_label.setText("Status: Completed")
            self.progress_bar.setValue(100)
            self.scraper.stop()
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(False)
            self.stop_button.setEnabled(False)

    def display_data(self, data):
        if not data:
            return

        # Define the desired column order
        column_order = ["title", "upper_price", "lower_price", "link", "image_url", "condition", "shipping", "location"]

        # Set the column count based on the number of desired columns
        self.table.setColumnCount(len(column_order))

        # Set the headers in the QTableWidget
        self.table.setHorizontalHeaderLabels(column_order)

        # Set the row count based on the data length
        self.table.setRowCount(len(data))

        # Populate the table with data according to the defined column order
        for row_idx, row_data in enumerate(data):
            for col_idx, header in enumerate(column_order):
                # Set each item in the corresponding row and column, default to an empty string if the key is missing
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(row_data.get(header, ""))))

    def on_display_data_button_clicked(self):
        data = hf.load_data_from_csv()
        if data:
            self.display_data_signal.emit(data)
            self.display_data(data)
        else:
            self.status_label.setText("Status: No data found in existing CSV files")

    def sort_data(self):
        selected_algo = self.sort_algo_dropdown.currentText()
        selected_column = self.sort_column_dropdown.currentText()
        
        sorting = SortingAlgorithms(hf.load_data_from_csv())
        sorted_data = sorting.sort_data(selected_algo, selected_column)
        self.display_data(sorted_data)

    def search_data(self):
        search_term = self.search_input.text()
        selected_algo = self.search_algo_dropdown.currentText()
        selected_column = self.search_column_dropdown.currentText()
        filter_option = self.filter_dropdown.currentText()

        result = self.scraper.search_data(search_term, selected_algo, selected_column, filter_option)
        self.display_data(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScraperUI()
    window.show()
    sys.exit(app.exec_())
