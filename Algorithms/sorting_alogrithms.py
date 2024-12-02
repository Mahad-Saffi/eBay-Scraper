from time import time
import Modules.variables as var
class SortingAlgorithms:
    def __init__(self, data):
        self.data = data

    # Bubble Sort
    def bubble_sort(self, key):
        starting_time = time() * 1000
        n = len(self.data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.data[j][key] > self.data[j + 1][key]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
        ending_time = time() * 1000
        
        total_time = ending_time - starting_time
        return self.data, total_time


    # Selection Sort
    def selection_sort(self, key):
        starting_time = time() * 1000
        n = len(self.data)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.data[j][key] < self.data[min_idx][key]:
                    min_idx = j
            self.data[i], self.data[min_idx] = self.data[min_idx], self.data[i]
        ending_time = time() * 1000
        
        total_time = ending_time - starting_time
        return self.data, total_time


    # Insertion Sort
    def insertion_sort(self, key):
        starting_time = time() * 1000
        for i in range(1, len(self.data)):
            key_item = self.data[i]
            j = i - 1
            while j >= 0 and key_item[key] < self.data[j][key]:
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key_item
        ending_time = time() * 1000
        
        total_time = ending_time - starting_time
        return self.data, total_time


    # Merge Sort
    def merge_sort(self, key):
        starting_time = time() * 1000
        self.merge_sort_helper(self.data, key)
        ending_time = time() * 1000
        
        total_time = ending_time - starting_time
        return self.data, total_time

    def merge_sort_helper(self, data, key):
        if len(data) > 1:
            mid = len(data) // 2
            left_half = data[:mid]
            right_half = data[mid:]

            # Recursively split and sort the left and right halves
            self.merge_sort_helper(left_half, key)
            self.merge_sort_helper(right_half, key)

            # Merge the sorted halves
            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i][key] < right_half[j][key]:
                    data[k] = left_half[i]
                    i += 1
                else:
                    data[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                data[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                data[k] = right_half[j]
                j += 1
                k += 1
    



    # Quick Sort
    def quick_sort(self, key):
        starting_time = time() * 1000
        self.quick_sort_helper(0, len(self.data) - 1, key)
        ending_time = time() * 1000
        
        total_time = ending_time - starting_time
        return self.data, total_time

    def quick_sort_helper(self, low, high, key):
        if low < high:
            # Get the index of the pivot element
            pi = self.partition(low, high, key)

            # Recursively sort elements before and after the pivot
            self.quick_sort_helper(low, pi - 1, key)
            self.quick_sort_helper(pi + 1, high, key)

    def partition(self, low, high, key):
        pivot = self.data[high][key]
        i = low - 1
        
        for j in range(low, high):
            if self.data[j][key] < pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
                
        self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
        
        return i + 1
     

    def counting_sort(self, key):
        starting_time = time() * 1000
        if not self.data:
            return []

        # Check if the key is in any attribute having string values
        string_columns = [att.lower().replace(" ", "_") for att in var.STRING_ATTRIBUTES]
        
        if key in string_columns:
            count = [0] * 26  # Array to count occurrences of each letter
            length_of_output = 0

            for item in self.data:
                if key == "location":
                    item[key] = item[key].replace("from ", "")
                
                if key in item and item[key]:
                    char = item[key][0]  # Get the first character to sort by
                    
                    # Get their values in the range 0-25
                    if 'a' <= char <= 'z':  
                        index = ord(char) - ord('a')
                        count[index] += 1
                        length_of_output += 1
                    elif 'A' <= char <= 'Z':
                        index = ord(char) - ord('A')
                        count[index] += 1
                        length_of_output += 1

            for i in range(1, len(count)):
                count[i] += count[i - 1]

            output = [None] * length_of_output

            for item in self.data:
                if key in item and item[key]:
                    char = item[key][0] 
                    if 'a' <= char <= 'z':
                        index = ord(char) - ord('a')
                        output[count[index] - 1] = item
                        count[index] -= 1
                    elif 'A' <= char <= 'Z':
                        index = ord(char) - ord('A')
                        output[count[index] - 1] = item
                        count[index] -= 1

            # Add remaining items that don't start with a alphabet and concatenate with the sorted items
            remaining_items = [item for item in self.data if not (key in item and (('a' <= item[key][0] <= 'z') or ('A' <= item[key][0] <= 'Z')))]
            self.data = output + remaining_items

        else:
            # Handling numbers
            if all(isinstance(item[key], (int, float)) for item in self.data):
                # Convert floats to integers for better sorting
                for item in self.data:
                    if key in item:
                        item[key] = int(round(item[key]))

                max_val = max(self.data, key=lambda x: x[key])[key]
                min_val = min(self.data, key=lambda x: x[key])[key]

                # Calculate the range of elements
                range_of_elements = int(max_val - min_val + 1)
                count = [0] * range_of_elements
                output = [None] * len(self.data)

                for item in self.data:
                    if key in item:
                        count_index = int(item[key] - min_val)
                        count[count_index] += 1

                for i in range(1, len(count)):
                    count[i] += count[i - 1]

                for item in reversed(self.data):
                    count_index = int(item[key] - min_val)
                    output[count[count_index] - 1] = item
                    count[count_index] -= 1

                self.data = output

        total_time = time() * 1000 - starting_time
        return self.data, total_time



    def counting_sort_radix(self, key, exp):
        if not self.data:
            return []
        
        # Handling numbers
        if all(isinstance(item[key], (int, float)) for item in self.data if key in item):
            count = [0] * 10  # Array to count occurrences of digits (0-9)
            output = [None] * len(self.data)

            for item in self.data:
                if key in item:
                    if isinstance(item[key], (int, float)):
                        digit = (int(item[key]) // exp) % 10
                        count[digit] += 1

            for i in range(1, len(count)):
                count[i] += count[i - 1]

            for item in reversed(self.data):
                if key in item and isinstance(item[key], (int, float)):
                    digit = (int(item[key]) // exp) % 10
                    output[count[digit] - 1] = item
                    count[digit] -= 1

            self.data = output

        return self.data


    def radix_sort(self, key):
        starting_time = time() * 1000
        if not self.data:
            return []

        # Check if the key is in any item
        if not any(key in item for item in self.data):
            print(f"Warning: The key '{key}' is not present in any items.")
            return self.data 
    
        numeric_items = [item for item in self.data if key in item and isinstance(item[key], (int, float))]
        
        for item in numeric_items:
            item[key] = int(round(item[key]))
        
        if numeric_items: 
            max_val = max(item[key] for item in numeric_items)
            exp = 1
            while max_val // exp > 0:
                self.counting_sort_radix(key, exp)
                exp *= 10
                
        ending_time = time() * 1000
        total_time = ending_time - starting_time

        return self.data, total_time 



    def bucket_sort(self, key):
        starting_time = time() * 1000
        if not self.data: 
            return []

        if not all(isinstance(item[key], float) for item in self.data if key in item):
            print("Warning: All items must have a float value for the selected key.")
            return self.data, 0

        # Create buckets
        max_val = max(item[key] for item in self.data if key in item)
        min_val = min(item[key] for item in self.data if key in item)
        bucket_count = 10  
        bucket_range = (max_val - min_val) / bucket_count
        buckets = [[] for _ in range(bucket_count)]

        for item in self.data:
            if key in item:
                if bucket_range == 0: 
                    index = bucket_count - 1
                else:
                    index = int((item[key] - min_val) // bucket_range)
                    index = min(index, bucket_count - 1)  
                
                buckets[index].append(item)

        sorted_data = []
        for bucket in buckets:
            sorted_data.extend(sorted(bucket, key=lambda x: x[key]))

        self.data = sorted_data  
        ending_time = time() * 1000
        
        total_time = ending_time - starting_time
        
        return self.data, total_time  

    
    def heap_sort(self, key):
        starting_time = time() * 1000
        n = len(self.data)

        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i, key)

        for i in range(n - 1, 0, -1):
            self.data[i], self.data[0] = self.data[0], self.data[i]  # Swap
            self.heapify(i, 0, key)
        ending_time = time() * 1000
        
        total_time = ending_time - starting_time
        return self.data, total_time

    def heapify(self, n, i, key):
        largest = i 
        left = 2 * i + 1
        right = 2 * i + 2 

        # Check if left child exists and is greater than root
        if left < n and self.data[left][key] > self.data[largest][key]:
            largest = left

        # Check if right child exists and is greater than the largest so far
        if right < n and self.data[right][key] > self.data[largest][key]:
            largest = right

        # If largest is not root, swap and continue heapifying
        if largest != i:
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            self.heapify(n, largest, key)
    
    
    def comb_sort(self, key):
        starting_time = time() * 1000
        n = len(self.data)
        gap = n
        shrink = 1.3  # Common shrink factor
        sorted = False

        while not sorted:
            # Update the gap for the next iteration
            gap = int(gap / shrink)
            if gap <= 1:
                gap = 1
                sorted = True

            # Perform a "bubble sort" pass with the current gap
            i = 0
            while i + gap < n:
                if self.data[i][key] > self.data[i + gap][key]:
                    self.data[i], self.data[i + gap] = self.data[i + gap], self.data[i]
                    sorted = False
                i += 1
        ending_time = time() * 1000
        
        total_time = ending_time - starting_time
        return self.data, total_time
    
    
    def shell_sort(self, key):
        starting_time = time() * 1000
        n = len(self.data)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = self.data[i]
                j = i
                while j >= gap and self.data[j - gap][key] > temp[key]:
                    self.data[j] = self.data[j - gap]
                    j -= gap

                self.data[j] = temp
            gap //= 2  
        ending_time = time() * 1000
        
        total_time = ending_time - starting_time
        return self.data, total_time





    # General method to sort based on the selected algorithm
    def sort_data(self, algo, column):
        if not self.data:
            return []
        
        key = column.lower().replace(" ", "_")

        if algo == "Bubble Sort":
            return self.bubble_sort(key)
        elif algo == "Selection Sort":
            return self.selection_sort(key)
        elif algo == "Insertion Sort":
            return self.insertion_sort(key)
        elif algo == "Merge Sort":
            return self.merge_sort(key)
        elif algo == "Quick Sort":
            return self.quick_sort(key)
        elif algo == "Counting Sort":
            return self.counting_sort(key)
        elif algo == "Radix Sort":
            return self.radix_sort(key)
        elif algo == "Bucket Sort":
            return self.bucket_sort(key)
        elif algo == "Heap Sort":
            return self.heap_sort(key)
        elif algo == "Comb Sort":
            return self.comb_sort(key)
        elif algo == "Shell Sort":
            return self.shell_sort(key)
        else:
            return self.data
