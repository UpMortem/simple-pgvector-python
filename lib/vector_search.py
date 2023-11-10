from sqlalchemy import create_engine, Column, Integer, String, JSON, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pgvector.sqlalchemy
from typing import List, Dict, Optional

# Set the vector dimension
VECTOR_DIMENSION = 1536

# Default number of top-k results
TOPK_DEFAULT = 50

Base = declarative_base()

class VectorItem(Base):
    __tablename__ = 'vector_items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    vector = Column(pgvector.sqlalchemy.VectorType(dimension=VECTOR_DIMENSION))  # Vector column with 1536 dimensions
    metadata = Column(JSON)  # JSON column for metadata

def initialize_database(database_url, namespace=None):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    if namespace:
        try:
            # Check if the schema (namespace) exists; if not, create it
            engine.execute(f"CREATE SCHEMA IF NOT EXISTS {namespace}")
            session.execute(f"SET search_path TO {namespace}")
        except exc.SQLAlchemyError as e:
            session.close()
            raise e

    return session

def add_vector_item(session, name: str, vector: List[float], metadata: Optional[Dict[str, str]] = None):
    try:
        item = VectorItem(name=name, vector=vector, metadata=metadata)
        session.add(item)
        session.commit()
        session.refresh(item)
    except IntegrityError:
        # Item with the same name already exists, update it
        existing_item = session.query(VectorItem).filter(VectorItem.name == name).one()
        existing_item.vector = vector
        existing_item.metadata = metadata
        session.commit()

def delete_vector_item(session, name: str):
    try:
        item = session.query(VectorItem).filter(VectorItem.name == name).one()
        session.delete(item)
        session.commit()
        return True
    except NoResultFound:
        # Item with the specified name doesn't exist
        return False

def query_vectors(session, query_vector, limit=TOPK_DEFAULT):
    return session.query(VectorItem).order_by(VectorItem.vector.pgvector_distance(query_vector)).limit(limit).all()

