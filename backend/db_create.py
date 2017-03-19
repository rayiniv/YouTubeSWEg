import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Video(Base):
	__tablename__ = "video"
	id = Column(Integer, primary_key = True)

	title = Column(String(250), nullable = False)
	description = Column(String(250), nullable = False)
	thumbnail = Column(String(250), nullable = False)
	tags = Column(String(250), nullable = False)
