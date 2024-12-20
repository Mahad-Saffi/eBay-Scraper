import re
import os
import pandas as pd
import Modules.variables as var

# Function to parse price and handle price range
def parse_price(price_text):
    price_pattern = re.compile(r"\$(\d+\.?\d*)\s*(?:to\s*\$(\d+\.?\d*))?")
    match = price_pattern.search(price_text)
    if match:
        lower_price = float(match.group(1))
        upper_price = float(match.group(2)) if match.group(2) else lower_price
        return lower_price, upper_price
    return None, None

# Formatting the shipping text
def classify_shipping(shipping_text):
    print(shipping_text)
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
    return "Not Found"

# Function to get the item name from the url
def get_item_name(url):
    match = re.search(r'_nkw=([^&]+)', url)
    if match:
        return match.group(1)
    return None

# Function to get the page number from the url
def increment_page_no(url):
    match = re.search(r'_pgn=(\d+)', url)
    
    if match:
        page_no = int(match.group(1))
        page_no += 1
        return re.sub(r'_pgn=\d+', f'_pgn={page_no}', url)
    return None


# Function to concatenate all CSV files in the data directory
def concatenate_csv_files(directory):
    try:
        concatenated_data = []
        # Define the standard header order
        headers_order = [att.lower().replace(" ", "_") for att in var.ATTRIBUTES]  # Add all relevant headers in the desired order

        # Traverse the main data directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == "data.csv":
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
                    
                    # Reorder columns to match the header order
                    df = df.reindex(columns=headers_order)
                    
                    concatenated_data.append(df)

        if concatenated_data:
            combined_df = pd.concat(concatenated_data, ignore_index=True)
            return combined_df.to_dict(orient='records')
        return []
    except Exception as e:
        print(f"Error concatenating CSV files: {e}")
        return []


def load_data_from_csv():
    directory = var.DIRECTORY
    try:
        if os.path.exists(directory):
            data = concatenate_csv_files(directory)
            print("Loaded existing data from CSV files.")
            return data
        else:
            print("No CSV files found in the directory.")
            return None
    except Exception as e:
        print(f"Error loading data from CSV: {e}")
        return None