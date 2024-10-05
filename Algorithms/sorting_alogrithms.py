class SortingAlgorithms:
    def __init__(self, data):
        self.data = data

    # Bubble Sort
    def bubble_sort(self, key):
        n = len(self.data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.data[j][key] > self.data[j + 1][key]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
        return self.data

    # Selection Sort
    def selection_sort(self, key):
        n = len(self.data)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.data[j][key] < self.data[min_idx][key]:
                    min_idx = j
            self.data[i], self.data[min_idx] = self.data[min_idx], self.data[i]
        return self.data

    # Insertion Sort
    def insertion_sort(self, key):
        for i in range(1, len(self.data)):
            key_item = self.data[i]
            j = i - 1
            while j >= 0 and key_item[key] < self.data[j][key]:
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key_item
        return self.data

    # Merge Sort
    def merge_sort(self, key):
        if len(self.data) > 1:
            mid = len(self.data) // 2
            left_half = self.data[:mid]
            right_half = self.data[mid:]

            # Recursively split and sort
            self.merge_sort_helper(left_half, key)
            self.merge_sort_helper(right_half, key)

            # Merge the sorted halves
            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i][key] < right_half[j][key]:
                    self.data[k] = left_half[i]
                    i += 1
                else:
                    self.data[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                self.data[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                self.data[k] = right_half[j]
                j += 1
                k += 1

        return self.data

    def merge_sort_helper(self, data, key):
        if len(data) > 1:
            mid = len(data) // 2
            left_half = data[:mid]
            right_half = data[mid:]

            # Recursively split and sort
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
        self.quick_sort_helper(0, len(self.data) - 1, key)
        return self.data

    def quick_sort_helper(self, low, high, key):
        if low < high:
            pi = self.partition(low, high, key)

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
        # Check if the data is numeric
        if all(isinstance(item[key], (int, float)) for item in self.data):
            # Handle numeric data
            values = [int(item[key]) for item in self.data]  # Convert to int
            max_val = max(values)  # Find the maximum numeric value
            count = [0] * (max_val + 1)
            output = [None] * len(self.data)

            # Count occurrences of each value
            for value in values:
                count[value] += 1

            # Update the count array to hold the actual position
            for i in range(1, len(count)):
                count[i] += count[i - 1]

            # Build the output array
            for i in reversed(range(len(values))):
                output[count[values[i]] - 1] = self.data[i]
                count[values[i]] -= 1

        else:
            # Handle string data (use the existing implementation for strings)
            max_char = 256  # ASCII range
            count = [0] * max_char
            output = [None] * len(self.data)

            # Count occurrences of each character (first char of each string)
            for item in self.data:
                count[ord(item[key][0])] += 1

            # Update the count array to hold the actual position
            for i in range(1, max_char):
                count[i] += count[i - 1]

            # Build the output array
            for item in reversed(self.data):
                char_index = ord(item[key][0])
                output[count[char_index] - 1] = item
                count[char_index] -= 1

        # Copy the sorted values back to self.data
        self.data[:] = output  # Update the original data
        return self.data

    # Radix Sort
    def radix_sort(self, key):
        if all(isinstance(item[key], (int, float)) for item in self.data):
            max_val = max(int(item[key]) for item in self.data)
            exp = 1
            while max_val // exp > 0:
                self.counting_sort_radix(key, exp)
                exp *= 10
        else:
            # For string data, use the existing radix sort logic
            max_length = max(len(item[key]) for item in self.data)
            for exp in range(max_length - 1, -1, -1):
                self.counting_sort_radix(key, exp)
        return self.data

    def counting_sort_radix(self, key, exp):
        if all(isinstance(item[key], (int, float)) for item in self.data):
            # Numeric data handling
            n = len(self.data)
            output = [None] * n
            count = [0] * 10  # Base 10 for digits

            for item in self.data:
                index = (int(item[key]) // exp) % 10
                count[index] += 1

            for i in range(1, 10):
                count[i] += count[i - 1]

            for i in reversed(range(n)):
                index = (int(self.data[i][key]) // exp) % 10
                output[count[index] - 1] = self.data[i]
                count[index] -= 1

        else:
            # String data handling (existing implementation)
            n = len(self.data)
            output = [None] * n
            count = [0] * 256  # ASCII range

            for item in self.data:
                index = ord(item[key][exp]) if exp < len(item[key]) else 0
                count[index] += 1

            for i in range(1, 256):
                count[i] += count[i - 1]

            for i in reversed(range(n)):
                index = ord(self.data[i][key][exp]) if exp < len(self.data[i][key]) else 0
                output[count[index] - 1] = self.data[i]
                count[index] -= 1

        self.data[:] = output


    def bucket_sort(self, key):
        if not self.data:
            return []

        if all(isinstance(item[key], (int, float)) for item in self.data):
            # Numeric bucket sort
            values = [int(item[key]) for item in self.data]
            max_val = max(values)
            bucket_count = len(self.data) // 10 + 1
            buckets = [[] for _ in range(bucket_count)]

            for item in self.data:
                index = int(item[key]) * bucket_count // (max_val + 1)
                buckets[index].append(item)

            sorted_data = []
            for bucket in buckets:
                sorted_data.extend(sorted(bucket, key=lambda x: int(x[key])))

        else:
            # String bucket sort (use the existing implementation for strings)
            max_char = 256  # ASCII range
            bucket_count = max_char

            # Create buckets
            buckets = [[] for _ in range(bucket_count)]

            # Place items into buckets based on the first character of the key
            for item in self.data:
                index = ord(item[key][0])
                buckets[index].append(item)

            sorted_data = []
            for bucket in buckets:
                sorted_data.extend(sorted(bucket, key=lambda x: x[key]))

        self.data[:] = sorted_data
        return self.data
    
    # Heap Sort
    def heap_sort(self, key):
        n = len(self.data)

        # Build a maxheap
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i, key)

        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            self.data[i], self.data[0] = self.data[0], self.data[i]  # Swap
            self.heapify(i, 0, key)

        return self.data

    def heapify(self, n, i, key):
        largest = i  # Initialize largest as root
        left = 2 * i + 1  # Left child
        right = 2 * i + 2  # Right child

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
            
    
    # Comb Sort
    def comb_sort(self, key):
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

        return self.data




    # General method to sort based on the selected algorithm
    def sort_data(self, algo, column):
        if not self.data:
            return []

        # Map column to internal representation (assuming data stores the attributes by their lower case keys)
        key = column.lower().replace(" ", "_")

        # Determine which algorithm to use
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
        else:
            # Default case or for other algorithms
            return self.data
