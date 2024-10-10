import sys
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QProgressBar, QComboBox, QTableWidget, QTableWidgetItem, 
                             QWidget, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from Modules.scraper_module import Scraper
from Algorithms.sorting_alogrithms import SortingAlgorithms
from Algorithms.searching_algorithms import SearchingAlgorithms
import Modules.variables as var
import Modules.helping_functions as hf


class ScraperUI(QMainWindow):
    # Define signals
    update_progress_signal = pyqtSignal(int)
    display_data_signal = pyqtSignal(list)
    update_button_signal = pyqtSignal(bool, bool, bool, bool)
    update_status_signal = pyqtSignal(str)
    
    
    # `````````````````````````````INITIALIZATION``````````````````````````````````
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eBay Scraper")
        self.setWindowIcon(QIcon(var.ICON_PATH))
        self.setGeometry(300, 300, 900, 900)
        self.setMaximumSize(900, 900)

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

        # Initially disable buttons except start button
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
        self.sort_column_dropdown.addItems(var.ATTRIBUTES)
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
        self.search_column_dropdown.addItems(var.ATTRIBUTES)
        self.search_input = QLineEdit("Enter Search Term")
        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(var.FILTER_OPTIONS)
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
        self.table.setColumnCount(len(var.ATTRIBUTES))
        self.table.setHorizontalHeaderLabels(var.ATTRIBUTES)
        layout.addWidget(self.table)
        self.display_data_button = QPushButton("Display Data")
        layout.addWidget(self.display_data_button)
        self.time_taken_label = QLabel("Time Taken: ")
        self.lower_status_label = QLabel("Status: ")
        layout.addWidget(self.time_taken_label)
        layout.addWidget(self.lower_status_label)

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
        self.update_button_signal.connect(self.update_buttons)
        self.update_status_signal.connect(self.update_status)




    # `````````````````````````````SCRAPING```````````````````````````````
    
    def start_scraping(self):
        self.progress_bar.setValue(0)
        
        item_name = self.item_input.text().replace(" ", "+")
        item_url = self.url_input.text()
        max_items = int(self.max_items_input.text()) if self.max_items_input.text().isdigit() else var.DEFAULT_MAX_ITEMS

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
        self.scraper.update_button_signal.connect(self.update_button_signal.emit)
        self.scraper.update_status_signal.connect(self.update_status_signal.emit)

        threading.Thread(target=self.run_scraper).start()

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
            
      
      
            
    # `````````````````````````````UPDATE UI COMPONENTS````````````````````````````````
    
    def update_status(self, status):
        self.lower_status_label.setText(f"Status: {status}")
            
    def update_buttons(self, start_button, pause_button, resume_button, stop_button):
        self.start_button.setEnabled(start_button)
        self.pause_button.setEnabled(pause_button)
        self.resume_button.setEnabled(resume_button)
        self.stop_button.setEnabled(stop_button)

    def update_progress(self, progress):
        self.progress_bar.setValue(int(progress))
        if progress >= 100:
            self.status_label.setText("Status: Completed")
            self.progress_bar.setValue(100)
            self.scraper.stop()
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(False)
            self.stop_button.setEnabled(False)




    
    # ````````````````````````````DISPLAY DATA```````````````````````````````
    
    def display_data(self, data):
        if not data:
            self.table.clearContents()
            return

        column_order = [att.lower().replace(" ", "_") for att in var.ATTRIBUTES]

        self.table.setColumnCount(len(column_order))

        self.table.setHorizontalHeaderLabels(column_order)

        self.table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            for col_idx, header in enumerate(column_order):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(row_data.get(header, ""))))

    def on_display_data_button_clicked(self):
        self.status_label.setText("Status: Loading data...")
        threading.Thread(target=self.run_display_data).start()

    def run_display_data(self):
        try:
            data = hf.load_data_from_csv()

            if not data:
                self.update_status_signal.emit("No data found in existing CSV files")
                return
            
            self.display_data_signal.emit(data)
            self.update_status_signal.emit("Data loaded successfully")
        except Exception as e:
            self.update_status_signal.emit(f"Error loading data: {e}")






    # ````````````````````````````````SORTING AND SEARCHING````````````````````````````
    def sort_data(self):
        self.status_label.setText("Status: Sorting...")
        threading.Thread(target=self.run_sort_data).start()

    def run_sort_data(self):
        try:
            selected_algo = self.sort_algo_dropdown.currentText()
            
            # If Radix sort is not already selected, remove all string columns from the dropdown and select the first numeric column
            if var.CURRENT_SORTING_ALGORITHM != "radix_sort" and selected_algo.lower().replace(" ", "_") == "radix_sort":
                # Remove all string columns from the dropdown
                self.sort_column_dropdown.clear()
                self.sort_column_dropdown.addItems([att for att in var.ATTRIBUTES if att not in var.STRING_ATTRIBUTES])
                self.sort_column_dropdown.setCurrentIndex(0)
                
            if var.CURRENT_SORTING_ALGORITHM != "bucket_sort" and selected_algo.lower().replace(" ", "_") == "bucket_sort":
                self.sort_column_dropdown.clear()
                self.sort_column_dropdown.addItems([att for att in var.ATTRIBUTES if att not in var.STRING_ATTRIBUTES])
                self.sort_column_dropdown.setCurrentIndex(0)
                
            # Else select the column from dropdown
            selected_column = self.sort_column_dropdown.currentText()
            var.CURRENT_SORTING_ALGORITHM = selected_algo.lower().replace(" ", "_")

            sorting = SortingAlgorithms(hf.load_data_from_csv())
            sorted_data, total_time_taken = sorting.sort_data(selected_algo, selected_column)

            self.time_taken_label.setText(f"Time Taken: {total_time_taken} milliseconds")
            self.display_data_signal.emit(sorted_data)
            self.status_label.setText("Status: Sorted successfully")
        except Exception as e:
            print("Error: ", e)
            self.update_status_signal.emit(f"Invalid column or sorting algorithm: {e}")


    def search_data(self):
        self.status_label.setText("Status: Searching...")
        threading.Thread(target=self.run_search_data).start()

    def run_search_data(self):
        try:
            search_term = self.search_input.text()
            selected_algo = self.search_algo_dropdown.currentText().lower()
            selected_column = self.search_column_dropdown.currentText().lower()
            filter_option = self.filter_dropdown.currentText().lower()

            searching = SearchingAlgorithms(hf.load_data_from_csv())
            result = searching.search_data(selected_column, search_term, selected_algo, filter_option)

            self.display_data_signal.emit(result)
        except Exception as e:
            print("Error: ", e)
            self.update_status_signal.emit(f"Invalid search term or column: {e}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScraperUI()
    window.show()
    sys.exit(app.exec_())
