from math import floor

class SearchingAlgorithms:
    def __init__(self, data):
        self.data = data

    # Linear Search
    def linear_search(self, key, search_term, option="contains"):
        results = []

        for item in self.data:
            value = item[key]

            # Handle cases where the value is not a string (int or float)
            if isinstance(value, (int, float)):
                # Convert the search term to the same type as value
                if isinstance(search_term, str):
                    try:
                        search_term = type(value)(search_term)
                    except ValueError:
                        continue    # Skip further processing for invalid search terms
                if isinstance(search_term, (int, float)):
                    if option == "contains" and floor(search_term) == floor(value):
                        results.append(item)
                    elif option == "starts with" and search_term == floor(value):
                        results.append(item)
                    elif option == "ends with" and search_term == round((value - floor(value)) * 100, 2): # Extract the decimal part
                        results.append(item)
                continue  # Skip further processing for non-string values
            
            # Convert value to string for string-based comparison
            value = str(value)

            # Split the value into words for comparison
            for word in value.split():
                if option == "contains" and search_term == word:
                    results.append(item)
                    break
                elif option == "starts with" and value.split()[0] == search_term:
                    results.append(item)
                    break
                elif option == "ends with" and value.split()[-1] == search_term:
                    results.append(item)
                    break

        return results


    def binary_search(self, key, search_term, option="contains"):
        # Ensure the data is sorted for binary search
        self.data.sort(key=lambda x: x[key])

        low, high = 0, len(self.data) - 1
        results = []

        while low <= high:
            mid = (low + high) // 2
            value = self.data[mid][key]

            # Handle cases where the value is not a string (int or float)
            if isinstance(value, (int, float)):
                # Convert the search term to the same type as value
                if isinstance(search_term, str):
                    try:
                        search_term = type(value)(search_term)
                    except ValueError:
                        low = mid + 1  # Invalid search term, continue the binary search
                        continue

                if isinstance(search_term, (int, float)):
                    # Check for matches with numeric criteria
                    if option == "contains" and floor(search_term) == floor(value):
                        results.append(self.data[mid])
                        break  # You can remove this `break` to continue searching adjacent items
                        
                    elif option == "starts with" and search_term == floor(value):
                        results.append(self.data[mid])
                        break  # You can remove this `break` to continue searching adjacent items
                        
                    elif option == "ends with" and search_term == round((value - floor(value)) * 100, 2):  # Extract decimal part
                        results.append(self.data[mid])
                        break  # You can remove this `break` to continue searching adjacent items

                # Modify the search range for binary search based on numeric comparison
                if search_term < value:
                    high = mid - 1
                else:
                    low = mid + 1

                continue  # Skip further string-based processing

            # Convert value to string for string-based comparison
            value = str(value)

            # Perform string-based binary search
            if option == "contains" and search_term in value:
                results.append(self.data[mid])
                break  # For "contains," we may have just one match in binary search

            elif option == "starts with" and value.startswith(search_term):
                results.append(self.data[mid])
                break  # For "startswith," break when a match is found

            elif option == "ends with" and value.endswith(search_term):
                results.append(self.data[mid])
                break  # For "endswith," break when a match is found

            # Modify the search range for binary search based on string comparison
            if search_term < value:
                high = mid - 1
            else:
                low = mid + 1

        # After the main loop, continue checking left and right of the found match for adjacent matches
        # Check left side
        left = mid - 1
        while left >= 0:
            value_left = self.data[left][key]

            # Handle numeric cases for left-side items
            if isinstance(value_left, (int, float)):
                if isinstance(search_term, (int, float)):
                    if option == "contains" and floor(search_term) == floor(value_left):
                        results.append(self.data[left])
                    elif option == "starts with" and search_term == floor(value_left):
                        results.append(self.data[left])
                    elif option == "ends with" and search_term == round((value_left - floor(value_left)) * 100, 2):
                        results.append(self.data[left])
                else:
                    break  # Stop if no more matches on the left side
            else:
                value_left = str(value_left)
                if (option == "contains" and search_term in value_left) or \
                (option == "starts with" and value_left.startswith(search_term)) or \
                (option == "ends with" and value_left.endswith(search_term)):
                    results.append(self.data[left])
                else:
                    break  # Stop if no more matches on the left side

            left -= 1

        # Check right side
        right = mid + 1
        while right < len(self.data):
            value_right = self.data[right][key]

            # Handle numeric cases for right-side items
            if isinstance(value_right, (int, float)):
                if isinstance(search_term, (int, float)):
                    if option == "contains" and floor(search_term) == floor(value_right):
                        results.append(self.data[right])
                    elif option == "starts with" and search_term == floor(value_right):
                        results.append(self.data[right])
                    elif option == "ends with" and search_term == round((value_right - floor(value_right)) * 100, 2):
                        results.append(self.data[right])
                else:
                    break  # Stop if no more matches on the right side
            else:
                value_right = str(value_right)
                if (option == "contains" and search_term in value_right) or \
                (option == "starts with" and value_right.startswith(search_term)) or \
                (option == "ends with" and value_right.endswith(search_term)):
                    results.append(self.data[right])
                else:
                    break  # Stop if no more matches on the right side

            right += 1

        return results


    
    def search_data(self, key, search_term, algorithm="linear search", option="contains"):
        key = key.lower().replace(" ", "_")
        algorithm = algorithm.lower()
        option = option.lower()
        
        if algorithm == "linear search":
            return self.linear_search(key, search_term, option)
        elif algorithm == "binary search":
            return self.binary_search(key, search_term, option)
        else:
            return "Invalid algorithm"
