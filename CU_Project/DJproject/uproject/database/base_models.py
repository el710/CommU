"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "Key_table"
    id = Column(Integer, primary_key=True, index=True)
    commu = Column(String)
    
    data_link = relationship(argument="DataModel", back_populates="commu_link")

class DataModel(Base):
    __tablename__ = "Data_table"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String)

    commu_link = relationship(argument="UserModel", back_populates="data_link")
    
    
