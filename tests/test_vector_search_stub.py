import unittest
import random
from stubs.vector_search import VectorSearchStub  # Replace 'your_module' with the actual module name

class TestVectorSearchStub(unittest.TestCase):
    def setUp(self):
        # Create an instance of VectorSearchStub for testing
        self.vector_search = VectorSearchStub()

    def test_add_vector_item_stub(self):
        # Add a vector item
        name = "Item 1"
        vector = self.vector_search.generate_random_vector()
        metadata = {"key1": "value1", "key2": "value2"}
        self.vector_search.add_vector_item_stub(name, vector, metadata)

        # Check if the item was added or updated correctly
        added_item = self.vector_search.vector_items[0]
        self.assertEqual(added_item['name'], name)
        self.assertEqual(added_item['vector'], vector)
        self.assertEqual(added_item['metadata'], metadata)

    def test_delete_vector_item_stub(self):
        # Add some vector items
        name1 = "Item 1"
        name2 = "Item 2"
        vector1 = self.vector_search.generate_random_vector()
        vector2 = self.vector_search.generate_random_vector()
        self.vector_search.add_vector_item_stub(name1, vector1)
        self.vector_search.add_vector_item_stub(name2, vector2)

        # Delete one of the items
        self.vector_search.delete_vector_item_stub(name1)

        # Check if the item was deleted correctly
        remaining_items = [item['name'] for item in self.vector_search.vector_items]
        self.assertNotIn(name1, remaining_items)
        self.assertIn(name2, remaining_items)

    def test_query_vectors_stub(self):
        # Add vector items
        names = ["Item 1", "Item 2", "Item 3"]
        vectors = [self.vector_search.generate_random_vector() for _ in range(3)]
        for name, vector in zip(names, vectors):
            self.vector_search.add_vector_item_stub(name, vector)

        # Query vectors
        query_vector = self.vector_search.generate_random_vector()
        results = self.vector_search.query_vectors_stub(query_vector, limit=2)

        # Check if the results are sorted and limited correctly
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0]['distance'] <= results[1]['distance'])

if __name__ == '__main__':
    unittest.main()

