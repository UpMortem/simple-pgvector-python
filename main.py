# main.py: This file shows you how to use this library.
import os
import numpy as np
from lib.vector_search import initialize_database, add_vector_item, query_vectors, delete_vector_item

# Get database credentials from environment variables with default values
db_username = os.environ.get('DB_USERNAME', 'your_default_username')
db_password = os.environ.get('DB_PASSWORD', 'your_default_password')
db_host = os.environ.get('DB_HOST', 'localhost')  # Provide a default host if not set
db_port = os.environ.get('DB_PORT', '5432')  # Provide a default port if not set
db_name = os.environ.get('DB_NAME', 'your_default_database_name')

# Define the database URL for SQLAlchemy
database_url = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'


# Define your database URL and namespace
namespace = 'mynamespace'  # Specify your desired namespace

# Initialize the database session
session = initialize_database(database_url, namespace=namespace)

def create_vector(dimensions=1536):
    # Generate a random vector with the specified dimensions (you can customize this)
    return list(np.random.rand(dimensions))

try:
    # Create a vector
    new_vector = create_vector()

    # Add the vector to the database
    add_vector_item(session, name='item3', vector=new_vector, metadata={'key': 'value'})

    # Query vector items
    query_vector = new_vector  # Use the created vector as the query vector
    results = query_vectors(session, query_vector)
    for result in results:
        print(f"Name: {result.name}, Vector: {result.vector}, Metadata: {result.metadata}")

    # Delete a vector item
    delete_result = delete_vector_item(session, name='item3')
    if delete_result:
        print("Item 'item3' deleted successfully.")
    else:
        print("Item 'item3' not found.")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    # Close the session
    session.close()

