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

    # Counting Sort
    def counting_sort(self, key):
        max_val = max(item[key] for item in self.data)
        count = [0] * (max_val + 1)
        output = [None] * len(self.data)

        for item in self.data:
            count[item[key]] += 1

        for i in range(1, len(count)):
            count[i] += count[i - 1]

        for item in reversed(self.data):
            output[count[item[key]] - 1] = item
            count[item[key]] -= 1

        self.data = output
        return self.data

    # Radix Sort
    def radix_sort(self, key):
        max_val = max(item[key] for item in self.data)
        exp = 1
        while max_val // exp > 0:
            self.counting_sort_radix(key, exp)
            exp *= 10
        return self.data

    def counting_sort_radix(self, key, exp):
        n = len(self.data)
        output = [None] * n
        count = [0] * 10

        for item in self.data:
            index = (item[key] // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in reversed(range(n)):
            index = (self.data[i][key] // exp) % 10
            output[count[index] - 1] = self.data[i]
            count[index] -= 1

        self.data = output

    # Bucket Sort
    def bucket_sort(self, key):
        if not self.data:
            return []

        max_val = max(item[key] for item in self.data)
        bucket_count = len(self.data) // 10 + 1
        buckets = [[] for _ in range(bucket_count)]

        for item in self.data:
            index = (item[key] * bucket_count) // (max_val + 1)
            buckets[index].append(item)

        for bucket in buckets:
            bucket.sort(key=lambda x: x[key])

        self.data = [item for bucket in buckets for item in bucket]
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
        else:
            # Default case or for other algorithms
            return self.data
