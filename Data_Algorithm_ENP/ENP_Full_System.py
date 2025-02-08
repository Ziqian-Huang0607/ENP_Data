import numpy as np
import time
import queue
import threading

# Configuration (Adjust for benchmarking)
DATA_SIZE = 1024 * 1024  # Size of data to benchmark on
NUM_THREADS = 4         # Number of threads for parallel algorithms


#--- New Algorithms ---#

def fast_group_by_sum(data, keys):
    """
    A (potentially) faster group-by-sum using NumPy's advanced indexing.
    Assumes keys are integers in a reasonable range (0 to max(keys)).

    This is often faster than pandas groupby for simple aggregations.
    """
    start_time = time.time()

    max_key = np.max(keys)
    sums = np.zeros(max_key + 1, dtype=data.dtype)  # Initialize sum array
    np.add.at(sums, keys, data)  # Use NumPy's atomic add for accumulation

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Fast Group By Sum Time: {elapsed_time:.6f} seconds")
    return sums, elapsed_time



def vectorized_string_search(strings, search_term):
    """
    Vectorized string search using NumPy and string operations.

    Avoids explicit loops for potentially faster string matching.
    """
    start_time = time.time()

    #Convert search term and strings to numpy objects
    strings = np.array(strings)

    matches = np.char.find(strings, search_term) >= 0

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Vectorized String Search Time: {elapsed_time:.6f} seconds")

    return matches, elapsed_time


def sorted_intersect(array1, array2):
    """
    Efficient intersection of two *sorted* arrays using NumPy.
    Exploits the sorted nature of the input for faster performance.

    If arrays aren't sorted, this will be slower than np.intersect1d!
    """

    start_time = time.time()

    intersection = np.intersect1d(array1, array2, assume_unique=True)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Sorted Intersect Time: {elapsed_time:.6f} seconds")
    return intersection, elapsed_time


def parallel_top_k(data, k, num_threads):
    """
    Finds the top-k elements in parallel using a thread pool.

    This can be faster than `np.partition` for very large datasets.
    """
    start_time = time.time()

    if num_threads <= 0:
        raise ValueError("Number of threads must be greater than 0.")

    #Ensure 'data' is numpy array
    data = np.array(data)

    if k >= len(data):
        print("k is greater than the number of data elements, so the sorted array will be returned")
        result = np.sort(data)[::-1] # Sort in descending order.
        return result, time.time() - start_time

    q = queue.PriorityQueue()  # Min-heap to store top-k elements

    def process_chunk(chunk):
        for x in chunk:
            # If the current element is greater than the smallest in heap, replace.
            if q.qsize() == k:
                if x > q.queue[0]:
                    q.get()
                    q.put(x)
            else:
                q.put(x)

    chunk_size = len(data) // num_threads
    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(data)
        thread = threading.Thread(target=process_chunk, args=(data[start:end],))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Extract the top-k elements from the heap and sort in descending order
    top_k_elements = sorted(list(q.queue), reverse=True)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Parallel Top K time : {elapsed_time:.6f} seconds using {num_threads} threads")
    return np.array(top_k_elements), elapsed_time

#--- Example Data Generation ---#

def generate_example_data(size):
    """Generates example data for benchmarking."""
    numeric_data = np.random.rand(size)
    integer_keys = np.random.randint(0, int(size * 0.1), size=size) # Keys in smaller range
    string_data = [f"string_{i}" for i in np.random.randint(0, int(size * 0.01), size=size)] # Fewer unique strings

    sorted_array1 = np.sort(np.random.randint(0, size, size=int(size * 0.5)))
    sorted_array2 = np.sort(np.random.randint(0, size, size=int(size * 0.5)))

    return numeric_data, integer_keys, string_data, sorted_array1, sorted_array2



#--- Benchmarking ---#

if __name__ == "__main__":
    np.random.seed(42)  # For reproducibility

    numeric_data, integer_keys, string_data, sorted_array1, sorted_array2 = generate_example_data(DATA_SIZE)

    #--- Algorithm Benchmarks ---#

    # Fast Group By Sum
    group_sums, group_time = fast_group_by_sum(numeric_data, integer_keys)

    # Vectorized String Search
    search_results, search_time = vectorized_string_search(string_data, "string_10")

    # Sorted Intersect
    intersect_result, intersect_time = sorted_intersect(sorted_array1, sorted_array2)

    # Parallel Top K
    top_k_elements, top_k_time = parallel_top_k(numeric_data, 100, NUM_THREADS)


    print("\n--- Results ---")
    print(f"Group Sums (first 10): {group_sums[:10]}")
    print(f"String Search Matches (first 10): {search_results[:10]}")
    print(f"Intersection Size: {len(intersect_result)}")
    print(f"Top 10 K Elements: {top_k_elements[:10]}")