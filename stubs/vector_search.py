import numpy as np
import random

class VectorSearchStub:
    def __init__(self, vector_dimension=1536):
        self.vector_dimension = vector_dimension
        self.vector_items = []

    def add_vector_item_stub(self, name, vector, metadata=None):
        existing_item = next((item for item in self.vector_items if item['name'] == name), None)
        if existing_item:
            # Update existing item
            existing_item['vector'] = vector
            if metadata is not None:
                existing_item['metadata'] = metadata
        else:
            # Create a new item
            id = len(self.vector_items) + 1
            item = {
                'id': id,
                'name': name,
                'vector': vector,
                'metadata': metadata if metadata is not None else {}
            }
            self.vector_items.append(item)

    def delete_vector_item_stub(self, name):
        self.vector_items = [item for item in self.vector_items if item['name'] != name]

    def query_vectors_stub(self, query_vector, limit=10):
        results = []
        for item in self.vector_items:
            distance = np.linalg.norm(np.array(query_vector) - np.array(item['vector']))
            results.append({'name': item['name'], 'distance': distance})  # Updated result format
        results.sort(key=lambda x: x['distance'])
        return results[:limit]  # Return a list of items with names and distances

    def generate_random_vector(self):
        return [random.uniform(0, 1) for _ in range(self.vector_dimension)]

