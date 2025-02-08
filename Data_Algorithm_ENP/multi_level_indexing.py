class MultiLevelIndex:
    def __init__(self, data):
        self.index = {}
        for i, value in enumerate(data):
            if value not in self.index:
                self.index[value] = []
            self.index[value].append(i)

    def query(self, value):
        return self.index.get(value, [])

# Example usage
data = [25, 25, 25, 30, 30, 35]
index = MultiLevelIndex(data)
print("Indices for value 25:", index.query(25))