import numpy as np

class ColumnarStorage:
    def __init__(self):
        self.columns = {}

    def add_column(self, name, data):
        # Compress data using run-length encoding
        compressed_data = []
        current_value = data[0]
        count = 1
        for value in data[1:]:
            if value == current_value:
                count += 1
            else:
                compressed_data.append((current_value, count))
                current_value = value
                count = 1
        compressed_data.append((current_value, count))
        self.columns[name] = compressed_data

    def get_column(self, name):
        # Decompress data
        compressed_data = self.columns[name]
        data = []
        for value, count in compressed_data:
            data.extend([value] * count)
        return np.array(data)

# Example usage
storage = ColumnarStorage()
storage.add_column('age', [25, 25, 25, 30, 30, 35])
print("Compressed Column:", storage.columns['age'])
print("Decompressed Column:", storage.get_column('age'))