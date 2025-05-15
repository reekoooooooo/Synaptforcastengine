class Memory:
    def __init__(self):
        self.storehouse = {}

    def store(self, key, value):
        self.storehouse[key] = value
        print(f"[Memory] Stored: {key}")

    def recall(self, key):
        return self.storehouse.get(key, "Memory not found.")
