import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON
from sqlalchemy.exc import IntegrityError
from pgvector.sqlalchemy import VectorType

# Get database credentials from environment variables
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')

# Define the database URL for SQLAlchemy
database_url = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

# Name of the table holding all vectors.
TABLE_NAME = "vector_items"
def create_table(table_name=TABLE_NAME, vector_dimension=1536):
    metadata = MetaData()

    vector_items_table = Table(
        table_name,
        metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('vector', VectorType(dimension=vector_dimension)),
        Column('metadata', JSON)
    )

    engine = create_engine(database_url)
    metadata.create_all(engine)

