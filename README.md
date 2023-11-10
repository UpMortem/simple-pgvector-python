
![PG](https://github.com/UpMortem/simple-pgvector-python/assets/469387/cd47dd3e-d8ae-44f7-a074-aa2c146a518b)

# Vector Search with Metadata

This project is a Python implementation for vector search with metadata using PostgreSQL and SQLAlchemy. It provides a flexible way to store vectors along with associated metadata, whether you are using PostgreSQL as your database or you want to test the functionality with in-memory data structures. It is very high level, so if you need finer level access just use pgvector-python directly rather than this library. This library is inspired by Pinecone's API for simplicity. Default for embeddings dimensions is that for Ada by OpenAI, however this is configurable in the code.

This library provides the following methods:
- Create a database
- Store vectors and metadata (upsert)
- Query for vectors based on similarity
- Delete vectors and metadata

## Features

- Store high-dimensional vectors along with metadata in a PostgreSQL database.
- Perform vector searches to find the closest vectors to a query vector.
- Flexible testing with stubs for in-memory testing without the need for a PostgreSQL database.

## Requirements

- Python 3.7+
- `numpy` for vector operations
- `sqlalchemy` for database interactions
- `pgvector` for PostgreSQL vector support

## Installation

1. Clone this repository:
   ```shell
   git clone https://github.com/yourusername/vector-search.git
   cd vector-search
   ```

## Creating the Database

Before running the application, you need to set up the database and create the necessary table to store vector data. Follow these steps to create the database:

1. **Database Setup**: Ensure that you have access to a PostgreSQL database server. You should have the following information ready:
   - Database host (e.g., localhost)
   - Database port (e.g., 5432)
   - Database name
   - Database username
   - Database password

2. **Set Environment Variables**: Use environment variables to securely store your database credentials. Create or modify an environment variables file (e.g., `.env`) and set the following variables with your actual credentials:
   - `DB_HOST`: The host or IP address of the database server.
   - `DB_PORT`: The port number to connect to the database.
   - `DB_NAME`: The name of the database.
   - `DB_USERNAME`: Your database username.
   - `DB_PASSWORD`: Your database password.

   You can set these environment variables manually or use a tool like [dotenv](https://pypi.org/project/python-dotenv/) to load them from a file.

```
from my_database_library.database import create_table

# Create a table with a namespace
create_table(vector_dimensions=1536)
```

3. **Run Database Creation Script**: Use the provided database creation script to create the necessary table in the database. Make sure you have PostgreSQL installed on your machine.

   ```bash
   python create_table.py
   ```

This script will create the vector_items table required for storing vector data.

Database Connection: Ensure that your application is configured to connect to the PostgreSQL database using the provided environment variables and the appropriate database URL.

Now, your database is set up, and the application is ready to use the PostgreSQL database to store and query vector data.

### Using the Vector Search Library
See main.py for an example of how to actually use the library.

If you have an existing Python script and you want to integrate the Vector Search Library into it for vector search functionality, follow these steps:

Installation: Ensure you have the necessary dependencies installed. You can install them using the provided requirements.txt file:

```
pip install -r requirements.txt
```

Import the Library: In your Python script, import the lib/vector_search.py module from this library. This module provides the vector search functionality.

```
from lib/vector_search import initialize_database, add_vector_item, query_vectors
```

Initialize the Database Connection: 

```
session = initialize_database(database_url, namespace="mynamespace")
```

#### Adding Vector Items
Use the add_vector_item function to add vector items to the database. Provide the name, vector, and optional metadata for each item.

```
name = "Item 1"
vector = [0.1, 0.2, 0.3, ...]  # Replace with your vector data
metadata = {"key1": "value1", "key2": "value2"}  # Optional metadata
add_vector_item(session, name, vector, metadata)
```

#### Querying Vectors
Use the query_vectors function to perform vector queries. Provide the query vector and specify the number of results (top-k) you want.

```
query_vector = [0.4, 0.5, 0.6, ...]  # Replace with your query vector data
limit = 10  # Number of results to retrieve (default is 50)
results = query_vectors(session, query_vector, limit=limit)
```

The results variable will contain the closest vector items based on your query.

#### Processing Results
Process the results as needed in your script. The results variable will contain information about the closest vector items, including their names, distances, and metadata.

Cleanup: Don't forget to close the database connection when you're done with it.

```
session.close()
```

Now, you can integrate the Vector Search Library into your existing Python script to add vector search capabilities to your application.

#### Run stub tests
```
python3 -m unittest tests.test_vector_search_stub
```

#### Run unit tests
```
python -m unittest tests/test_vector_search.py
```

## License
MIT Linense. Go nuts.
