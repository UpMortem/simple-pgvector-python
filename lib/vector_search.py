from sqlalchemy import create_engine, Column, Integer, String, JSON, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError, NoResultFound
import pgvector.sqlalchemy
from typing import List, Dict, Optional
import logging

# Set the vector dimension and default number of top-k results
VECTOR_DIMENSION = 1536
TOPK_DEFAULT = 50

Base = declarative_base()
logging.basicConfig(level=logging.DEBUG)

class VectorItem(Base):
    __tablename__ = 'vector_items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    vector = Column(pgvector.sqlalchemy.VectorType(dimension=VECTOR_DIMENSION))
    metadata = Column(JSON)

def initialize_database(database_url: str, namespace: Optional[str] = None) -> Session:
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    if namespace:
        # Validate namespace or use parameterized queries to prevent SQL Injection
        try:
            engine.execute("CREATE SCHEMA IF NOT EXISTS %s", (namespace,))
            engine.execute("SET search_path TO %s", (namespace,))
        except exc.SQLAlchemyError as e:
            logging.error("Error setting namespace: %s", e)
            raise

    return Session()

def add_vector_item(session: Session, name: str, vector: List[float], metadata: Optional[Dict[str, str]] = None) -> None:
    """ Adds a new vector item to the database. """
    try:
        item = VectorItem(name=name, vector=vector, metadata=metadata)
        session.add(item)
        session.commit()
        logging.info("Added new vector item: %s", name)
    except IntegrityError as e:
        logging.error("Error adding vector item: %s", e)
        session.rollback()
        raise

def update_vector_item(session: Session, name: str, vector: List[float], metadata: Optional[Dict[str, str]] = None) -> bool:
    """ Updates an existing vector item. """
    try:
        existing_item = session.query(VectorItem).filter(VectorItem.name == name).one()
        existing_item.vector = vector
        existing_item.metadata = metadata
        session.commit()
        logging.info("Updated vector item: %s", name)
        return True
    except NoResultFound:
        logging.error("Vector item not found: %s", name)
        return False

def delete_vector_item(session: Session, name: str) -> bool:
    try:
        item = session.query(VectorItem).filter(VectorItem.name == name).one()
        session.delete(item)
        session.commit()
        logging.info("Deleted vector item: %s", name)
        return True
    except NoResultFound:
        logging.error("Vector item not found: %s", name)
        return False

def query_vectors(session: Session, query_vector: List[float], limit: int = TOPK_DEFAULT) -> List[VectorItem]:
    """ Queries the vector items based on a given vector. """
    return session.query(VectorItem).order_by(VectorItem.vector.pgvector_distance(query_vector)).limit(limit).all()

