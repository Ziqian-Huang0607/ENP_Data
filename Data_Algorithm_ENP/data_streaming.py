class StreamingProcessor:
    def __init__(self):
        self.data = []

    def add_data(self, new_data):
        self.data.extend(new_data)
        # Process the new data (e.g., compute the mean)
        mean = sum(self.data) / len(self.data)
        print(f"New Data Added: {new_data}, Current Mean: {mean}")

# Example usage
processor = StreamingProcessor()
processor.add_data([10, 20])
processor.add_data([30, 40])