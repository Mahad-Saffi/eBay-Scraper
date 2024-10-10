import time
import Modules.helping_functions as hf

def getUrl(query="shoes", page_no=1):
    return f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={query}&_sacat=0&_pgn={page_no}"

def getDirectory(query):
    return f"data/{hf.get_item_name(query)}_{time.strftime('%Y%m%d_%H%M%S')}"



ICON_PATH = "Assets/icon.png"
DEFAULT_URL = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=shoes&_sacat=0&_pgn=1"
DEFAULT_MAX_ITEMS = 25000
STOPPING_SCRAPE_BEFORE_MIN_ITEMS = 6
DIRECTORY = "data"
ATTRIBUTES = ["Title", "Upper Price", "Lower Price", "Link", "Image Url", "Condition", "Shipping", "Location"]
STRING_ATTRIBUTES = ["Title", "Link", "Image Url", "Condition", "Shipping", "Location"] 
SORTING_ALGORITHMS = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Counting Sort", "Radix Sort", "Bucket Sort", "Heap Sort", "Comb Sort", "Shell Sort"]
SEARCHING_ALGORITHMS = ["Linear Search", "Binary Search"]
FILTER_OPTIONS = ["Contains", "Starts With", "Ends With"]
CURRENT_SORTING_ALGORITHM = "Bubble Sort"