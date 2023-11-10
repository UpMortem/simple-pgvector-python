import unittest
from unittest.mock import patch
from lib.vector_search import initialize_database, add_vector_item, update_vector_item, delete_vector_item, query_vectors
from sqlalchemy.orm import Session
from lib.vector_search import VectorItem
import pgvector

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        # Set up code for each test
        pass

    def tearDown(self):
        # Tear down code for each test
        pass

    @patch('lib.vector_search.create_engine')
    def test_initialize_database(self, mock_create_engine):
        session = initialize_database("test_database_url")
        self.assertIsInstance(session, Session)

    @patch('lib.vector_search.Session')
    def test_add_vector_item(self, mock_session):
        mock_session_instance = mock_session.return_value
        add_vector_item(mock_session_instance, "test_name", [0.1, 0.2], {"key": "value"})
        mock_session_instance.add.assert_called()
        mock_session_instance.commit.assert_called()

    @patch('lib.vector_search.Session')
    def test_update_vector_item(self, mock_session):
        mock_session_instance = mock_session.return_value
        mock_session_instance.query.return_value.filter.return_value.one.return_value = VectorItem()
        result = update_vector_item(mock_session_instance, "test_name", [0.3, 0.4], {"key": "value"})
        self.assertTrue(result)

    @patch('lib.vector_search.Session')
    def test_delete_vector_item(self, mock_session):
        mock_session_instance = mock_session.return_value
        mock_session_instance.query.return_value.filter.return_value.one.return_value = VectorItem()
        result = delete_vector_item(mock_session_instance, "test_name")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()

