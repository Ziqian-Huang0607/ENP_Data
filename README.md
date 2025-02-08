# High-Performance Algorithmic Benchmarks (Python)

This repository showcases several algorithm approaches designed for potential use in database systems (such as SAP HANA) to improve performance. The focus is on demonstrating the *algorithmic* principles, not on creating a production-ready database system.  The algorithms are implemented in Python for ease of understanding and experimentation, but it's crucial to recognize that **Python is not an efficient language for production database implementations.** C, C++, or other low-level languages would be necessary for optimal performance.

**Disclaimer:** This is an *example* implementation for educational and research purposes. The performance observed here may not directly translate to performance within a highly optimized database engine like SAP HANA. These implementations are intended to spark ideas for algorithmic improvements that could then be implemented in a more suitable language and integrated into a database system.

## Algorithms Included

### 1. Fast Group By Sum (Vectorized Accumulation)

*   **Description:** This algorithm provides a potentially faster approach to the "group by" and summation operation, a common task in data analysis. It leverages NumPy's advanced indexing and atomic addition (`np.add.at`) to efficiently accumulate sums for different key groups.  This avoids explicit loops and often outperforms naive implementations or even pandas `groupby` for simple aggregations.
*   **Algorithm:**
    1.  Determine the maximum key value in the `keys` array.
    2.  Initialize a `sums` array of zeros with a size one greater than the maximum key. The data type of this is the data type of the original data.
    3.  Use `np.add.at(sums, keys, data)` to atomically add the corresponding `data` values to the `sums` array based on the `keys`.
*   **Complexity:**
    *   Time: O(N), where N is the size of the data array (assuming `np.add.at` is O(1) on average for each element).
    *   Space: O(K), where K is the number of unique keys.
*   **Potential Use Cases:** Scenarios where the number of distinct keys is significantly smaller than the dataset size and fast aggregation is critical.
*   **Authorship & Inspiration:** The concept builds upon the principles of vectorized operations in NumPy.  `np.add.at` functionality is part of the NumPy library,  authored and maintained by the NumPy developers ([NumPy Website](https://numpy.org/)).  The specific application and optimization for group-by-sum are inspired by common data analysis patterns.
*   **Reference:**  NumPy documentation on `np.add.at` and advanced indexing.

### 2. Vectorized String Search (Regular Expression Matching)

*   **Description:** This algorithm performs a substring search within an array of strings. It uses Python's `re` (regular expression) module for efficient pattern matching.  Pre-compiling the regular expression provides significant performance benefits when the search term is constant across multiple searches. This can be faster than NumPy's built in string searching
*   **Algorithm:**
    1.  A regular expression is compiled from the search term.  Special characters in the search term are escaped to ensure a literal match.
    2.  List comprehension is used to iterate over the string array.
    3.  The `search` method of the regular expression pattern is used on each string.
    4.  The results are converted to a boolean array, indicating whether each string contains the substring or not.
*   **Complexity:**
    *   Time: Roughly O(N * M), where N is the number of strings and M is the average length of a string, although regular expressions are very complex.
    *   Space: O(1) (excluding the space for the input strings).
*   **Potential Use Cases:** Searching for specific patterns within text data, filtering string columns based on substring matches.
*   **Authorship & Inspiration:** Based on the use of Python's `re` module, which is part of the Python Standard Library and authored by the Python Software Foundation and contributors ([Python Website](https://www.python.org/)). Regular expression concepts are well-established in computer science.
*    **Reference:**
        *   Python `re` module documentation: [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)
        *   Friedl, J. E. F. (2006). *Mastering Regular Expressions* (3rd ed.). O'Reilly Media.

### 3. Sorted Intersect (NumPy `intersect1d` or Bisect)

*   **Description:**  This algorithm efficiently finds the intersection of two *sorted* arrays.  It leverages NumPy's `intersect1d` function, which is optimized for sorted inputs (when `assume_unique=True` is used), or a Binary search approach using bisect. These functions provide a more optimized intersect approach to finding the shared elements
*   **Algorithm:**
    1.  Input arrays must be sorted.
    2.  Call `np.intersect1d(array1, array2, assume_unique=True)` (NumPy version).
    3.  Alternatively, can use a binary search approach to determine the intersects.
*   **Complexity:**
    *   Time: O(N + M) on average (NumPy `intersect1d` with sorted arrays), or O(N*log(M)) (Binary Search approach), where N and M are the lengths of the input arrays.
    *   Space: O(min(N, M)) in the worst case (the size of the intersection).
*   **Potential Use Cases:** Finding common elements between sorted index lists, determining overlapping sets of IDs in sorted data.
*   **Authorship & Inspiration:** Based on NumPy's `intersect1d` function (NumPy developers) and binary search concepts (well-established in computer science).
*   **Reference:** NumPy documentation on `np.intersect1d`.

### 4. Parallel Top K (Priority Queue with Threading)

*   **Description:**  This algorithm finds the *k* largest elements in a dataset using a parallel approach with a priority queue (min-heap) and multiple threads. The min-heap helps reduce complexity from linear sort.
*   **Algorithm:**
    1.  Divide the input data into chunks, one for each thread.
    2.  Each thread maintains a local min-heap (priority queue) of size *k*.
    3.  Each thread iterates through its data chunk:
        *   If the current element is greater than the smallest element in the heap, replace the smallest element with the current element.
        *   Otherwise, discard the current element.
    4.  After all threads have processed their data, merge the *k* elements from each thread's heap into a final sorted list.
*   **Complexity:**
    *   Time: close to O(N log k) but heavily influenced by the thread count.
    *   Space: O(k)
*   **Potential Use Cases:** Ranking large datasets in parallel, finding the most frequent items in a distributed system.
*   **Authorship & Inspiration:** Inspired by parallel processing techniques and the use of priority queues for finding top-k elements. The threading is based on standard Python libraries.
*   **Reference:**
    *   Threading documentation

## Getting Started

1.  **Clone the repository:**  `git clone [repository URL]`
2.  **Install Dependencies:** `pip install numpy` (and optionally `cupy` and `numba` - see below)
3.  **Run the `ENP_Full_System.py` script:**  `/opt/miniconda3/envs/ISA_base/bin/python "/Users/windy/Documents/1 Gordon/Data_Algorithm_ENP/ENP_Full_System.py"`

## Optional Enhancements (If Desired)

*   **CuPy (GPU Acceleration):**  Install `cupy` (`pip install cupy-cuda12x` - adjust CUDA version as needed) to potentially accelerate certain operations on NVIDIA GPUs.  The code includes flags to enable/disable GPU usage. Note: If you don't have CUDA, install `cupy-cpu` for CPU-only operation but performance will be significantly reduced.
*   **Numba (JIT Compilation):**  Install `numba` (`pip install numba`) to potentially improve CPU performance through just-in-time (JIT) compilation. The code detects if Numba is installed and uses it automatically.
*   **NUMA Optimization (Advanced):** For systems with NUMA architecture, investigate the `numactl` tool to optimize memory allocation and thread placement.  This requires system-level configuration and is not included in the Python code directly.

## Important Notes

*   **Python Inefficiency:** The Python implementations are for demonstration *only*. Python's global interpreter lock (GIL) and interpreted nature limit its performance. A real database system would use a compiled language.
*   **Benchmarking is Crucial:**  Always benchmark the algorithms with *your specific data and query patterns* to determine if they provide performance benefits.  The provided benchmarks are just a starting point.
*   **Algorithm Selection:** The best algorithm depends on the characteristics of your data and the specific operation you are performing.  There is no "one size fits all" solution.
*   **Real-World Databases:** Highly optimized database systems like SAP HANA employ many sophisticated techniques (e.g., data compression, query optimization, caching) that are not covered in these simplified examples.

## Contributing

This is intended to be an open-source project. Contributions, including algorithm improvements, performance benchmarks, and detailed explanations, are welcome! Please submit pull requests with clear descriptions of your changes.
