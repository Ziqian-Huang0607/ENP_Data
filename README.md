# ENP: High-Performance Algorithmic Examples

This repository presents several algorithm approaches that can potentially be used in database systems (such as SAP HANA) to improve performance. The focus is on demonstrating the *algorithmic* principles.  This is *not* a production-ready database system.  The algorithms are implemented in Python for clarity and ease of experimentation. However, it's important to realize that **Python is not an efficient language for real-world database implementations.** C, C++, or other low-level languages would be needed for best performance.

**Disclaimer:** This is an *example* implementation for educational and research. The performance shown here might not apply to complex database systems like SAP HANA. These examples are intended to spark ideas for algorithmic improvements that could be implemented in a suitable language and integrated into a database system.

## Algorithms Included

### 1. Fast Group By Sum (Vectorized Accumulation)

*   **Description:** This algorithm provides a faster approach to the "group by" and summation operation common in data analysis. It leverages NumPy's advanced indexing and atomic addition (`np.add.at`) to efficiently accumulate sums for different key groups. This avoids explicit loops and can often outperform pandas `groupby` for simple aggregations.
*   **Algorithm:**
    1.  Find the maximum key value in the `keys` array.
    2.  Initialize a `sums` array of zeros with a size one greater than the maximum key.  The data type of this array matches the input data.
    3.  Use `np.add.at(sums, keys, data)` to atomically add the corresponding `data` values to the `sums` array based on the `keys`.
*   **Complexity:**
    *   Time: O(N), where N is the size of the data array (assuming `np.add.at` is O(1) on average per element).
    *   Space: O(K), where K is the number of unique keys.
*   **Potential Use Cases:** Scenarios where the number of distinct keys is significantly smaller than the dataset size and fast aggregation is critical.
*   **Authorship & Inspiration:** The concept uses the principles of vectorized operations in NumPy.  `np.add.at` functionality is part of the NumPy library,  authored and maintained by the NumPy developers ([NumPy Website](https://numpy.org/)).  The application and optimization for group-by-sum are inspired by typical data analysis patterns.
*   **Reference:**  NumPy documentation on `np.add.at` and advanced indexing.

### 2. Vectorized String Search (Regular Expression Matching)

*   **Description:** This algorithm performs a substring search within an array of strings. It uses Python's `re` (regular expression) module for efficient pattern matching.  Pre-compiling the regular expression provides performance benefits when the search term is constant across multiple searches. This can provide faster string searching compared to alternatives.
*   **Algorithm:**
    1.  A regular expression is compiled from the search term. Special characters in the search term are escaped to ensure a literal match.
    2.  List comprehension iterates over the string array.
    3.  The `search` method of the regular expression pattern is used on each string.
    4.  The results are converted to a boolean array, indicating if each string contains the substring.
*   **Complexity:**
    *   Time: Roughly O(N * M) where N is the number of strings and M is the average string length, *however*, regular expression complexity can vary significantly depending on the pattern.
    *   Space: O(1) (excluding the space for the input strings).
*   **Potential Use Cases:** Searching for patterns within text, filtering string columns based on substring matching.
*   **Authorship & Inspiration:** Based on Python's `re` module, part of the Python Standard Library authored by the Python Software Foundation and contributors ([Python Website](https://www.python.org/)). Regular expression concepts are well-established in computer science.
*    **Reference:**
        *   Python `re` module documentation: [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)
        *   Friedl, J. E. F. (2006). *Mastering Regular Expressions* (3rd ed.). O'Reilly Media.

### 3. Sorted Intersect (NumPy `intersect1d` or Bisect)

*   **Description:**  This algorithm finds the intersection of two *sorted* arrays efficiently.  It uses NumPy's `intersect1d` function, which is optimized for sorted inputs (when `assume_unique=True` is used), or a Binary search approach using bisect. The binary search approach offers another way to find intersects.
*   **Algorithm:**
    1.  Input arrays *must* be sorted.
    2.  Call `np.intersect1d(array1, array2, assume_unique=True)` (NumPy version) or use the bisect library approach.
*   **Complexity:**
    *   Time: O(N + M) on average (NumPy `intersect1d` with sorted arrays), or O(N*log(M)) (Bisect Method), where N and M are the input arrays' lengths.
    *   Space: O(min(N, M)) in the worst case (the size of the intersection).
*   **Potential Use Cases:** Finding common elements between sorted index lists, determining overlapping sets of IDs in sorted data.
*   **Authorship & Inspiration:** Based on NumPy's `intersect1d` function (NumPy developers) and binary search concepts (well-established).
*   **Reference:** NumPy documentation on `np.intersect1d` and documentation on `bisect`.

### 4. Parallel Top K (Priority Queue with Threading)

*   **Description:**  This algorithm finds the *k* largest elements in a dataset in parallel, using a priority queue (min-heap) and multiple threads.
*   **Algorithm:**
    1.  Divide the input data into chunks for each thread.
    2.  Each thread maintains a local min-heap (priority queue) of size *k*.
    3.  Each thread iterates through its chunk:
        *   If the current element is greater than the smallest in the heap, replace the smallest with the current element.
        *   Otherwise, discard the current element.
    4.  After all threads process their data, merge the *k* elements from each thread's heap into a final sorted list.
*   **Complexity:**
    *   Time: close to O(N log k) but is heavily influenced by thread count.
    *   Space: O(k)
*   **Potential Use Cases:** Ranking large datasets, finding frequent items in a distributed setting.
*   **Authorship & Inspiration:** Inspired by parallel processing and priority queues for top-k problems. Threading uses standard Python libraries.
*   **Reference:** Threading and priority queue documentation.

## Getting Started

1.  **Clone the repository:**  `git clone [repository URL]`
2.  **Install Dependencies:** `pip install numpy` (and optionally `cupy` and `numba` - see below)
3.  **Run the `ENP_Full_System.py` script:**  `python ENP_Full_System.py`

## Optional Enhancements

*   **CuPy (GPU Acceleration):**  Install `cupy` (`pip install cupy-cuda12x` - adjust CUDA version as needed) to potentially accelerate operations on NVIDIA GPUs.  The code includes flags to enable/disable GPU usage.  If you don't have CUDA, install `cupy-cpu` for CPU-only operation (significantly reduced performance).
*   **Numba (JIT Compilation):**  Install `numba` (`pip install numba`) to potentially improve CPU performance with just-in-time (JIT) compilation. The code detects and uses Numba automatically.
*   **NUMA Optimization (Advanced):** For NUMA systems, use `numactl` to optimize memory and thread placement. This requires system-level configuration.

## Important Notes

*   **Python Inefficiency:** The Python implementations are for *demonstration* purposes. Python's GIL and interpreted nature limit performance. Real databases would use a compiled language.
*   **Benchmarking:** Benchmark the algorithms with *your* data and queries to assess potential benefits.
*   **Algorithm Selection:** The best algorithm depends on data characteristics and the operation. No single solution fits all cases.
*   **Real-World Databases:** Optimized database systems like SAP HANA use data compression, query optimization, caching, etc., not covered here.

## Recorded Speed on Example System

Fast Group By Sum Time: 0.007817 seconds

Vectorized String Search Time: 0.409823 seconds

Sorted Intersect Time: 0.033284 seconds

Parallel Top K time : 0.651712 seconds using 4 threads

--- Results ---

Group Sums (first 10): [7.12579915 4.82668659 6.38690715 6.88517474 7.0372191  3.51176267

 6.92013293 3.5331242  7.30527909 2.00707586]
 
String Search Matches (first 10): [False False  True False False False False False False False]

Intersection Size: 386265

Top 10 K Elements: [0.99999831 0.99999493 0.99999461 0.99999282 0.99999204 0.99999125

 0.99999003 0.99998943 0.99998938 0.9999885 ]
 
## Contributing

This is intended to be an open-source project. Contributions, including algorithm improvements, benchmarks, and detailed explanations, are welcome!  Submit pull requests with clear descriptions.
Contact me: ziqian.huang@hotmail.com
