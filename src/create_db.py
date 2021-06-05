#!/usr/bin/env python3
import os
from pathlib import Path
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Float, String

app_data_path = Path.home() / '.picren'
os.makedirs(app_data_path, exist_ok=True)
adp_str = 'sqlite:///' + str(app_data_path) + '/location_cache.db'
engine = create_engine(adp_str) #, echo = True)
Base = declarative_base()

class Location(Base):
  __tablename__ = 'locations'
  longitude = Column(Float, primary_key=True, nullable=False)
  latitude = Column(Float, primary_key=True, nullable=False)
  address = Column(String, nullable=False)

Base.metadata.create_all(engine)

