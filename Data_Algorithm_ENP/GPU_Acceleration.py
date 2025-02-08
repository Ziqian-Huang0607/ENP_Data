import cupy as cp

def gpu_process(data):
    # Move data to GPU
    gpu_data = cp.array(data)
    # Perform a computation (e.g., square all elements)
    result = cp.square(gpu_data)
    # Move result back to CPU
    return cp.asnumpy(result)

# Example usage
data = np.array([1, 2, 3, 4, 5], dtype=np.float32)
print("Processed Data:", gpu_process(data))