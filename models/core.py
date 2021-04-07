import os

import sqlalchemy
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import Session

from .base import Base


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigDatabase(metaclass=Singleton):
    engine: Engine = None
    connection: Connection = None
    session: Session = None

    def __init__(self):
        hostname = os.environ['DB_HOST']
        user = os.environ['DB_USER']
        password = os.environ['DB_PASSWORD']
        dbname = os.environ['DB_NAME']
        port = os.environ['DB_PORT']

        self.engine = sqlalchemy.create_engine(f'postgresql://{user}:{password}@{hostname}:{port}/{dbname}')
        self.connection = self.engine.connect()
        self.session = Session(bind=self.connection)


class Extension(Base):
    __tablename__ = 'config_extension'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_active = Column(Boolean)
    created_at = Column(TIMESTAMP)


class File(Base):
    __tablename__ = 'config_file'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_processed = Column(Boolean, default=False)
    format = Column(String)
    separator = Column(String)
    created_at = Column(TIMESTAMP)


class Country(Base):
    __tablename__ = 'config_country'

    id = Column(Integer, primary_key=True)
    site = Column(String)
    identification = Column(String)
    is_processed = Column(Boolean)


class SearchRAW(Base):
    __tablename__ = 'data_search_fact'

    id = Column(Integer, primary_key=True)
    site = Column(String)
    identification = Column(String)
    category = Column(String)
    json_data = Column(JSONB)
    is_processed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)


class Items(Base):
    __tablename__ = 'data_items'

    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    start_time = Column(TIMESTAMP)
    name = Column(String)
    description = Column(String)
    nickname = Column(String)
