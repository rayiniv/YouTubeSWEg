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

class Channel(Base):
	__tablename__ = "channel"
	id = Column(Integer, primary_key = True)

	title = Column(String(250), nullable = False)
	description = Column(String(250), nullable = False)	
	published_date = Column(DateTime, default = None)
	country = Column(String(250), nullable = False)
	view_count = Column(BigInteger, nullable = False)
	subscriber_count = Column(BigInteger, nullable = False)

class Category(Base):
	__tablename__ = "category"
	id = Column(Integer, primary_key = True)

	title = Column(String(250), nullable = False)
	latest_published_date = Column(DateTime, default = None)
	num_videos = Column(Integer, nullable = False)
	assignable = Column(Boolean, unique = False, default = True)		
