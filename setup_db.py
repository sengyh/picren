from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Float, String

engine = create_engine('sqlite:///location_cache.db')#, echo = True)
Base = declarative_base()

class Location(Base):
  __tablename__ = 'locations'
  longitude = Column(Float, primary_key=True, nullable=False)
  latitude = Column(Float, primary_key=True, nullable=False)
  address = Column(String, nullable=False)

Base.metadata.create_all(engine)

