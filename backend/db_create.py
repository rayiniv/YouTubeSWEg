import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

video_category_table = Table('video_category', Base.metadata,
    Column('categories_id', Integer, ForeignKey('category.id')),
    Column('videos_id', Integer, ForeignKey('video.id'))
)

video_playlist_table = Table('video_playlist', Base.metadata,
    Column('playlists_id', Integer, ForeignKey('playlist.id')),
    Column('videos_id', Integer, ForeignKey('video.id'))
)

class Video(Base):
	__tablename__ = "video"
	id = Column(Integer, primary_key = True)

	title = Column(String(250), nullable = False)
	description = Column(String(250), nullable = False)
	thumbnail = Column(String(250), nullable = False)
	tags = Column(String(250), nullable = False)

	channel_id = Column(Integer, ForeignKey('channel.id'))
	channel = relationship("Channel", back_populates="videos")

	categories = relationship("Category", secondary = video_category_table, back_populates = "videos")

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

class Playlist(Base):
	__tablename__ = "playlist"
	id = Column(Integer, primary_key = True)

	title = Column(String(250), nullable = False)
	description = Column(String(250), nullable = False)
	tags = Column(String(250), nullable = False)
	published_date = Column(DateTime, default = None)
	num_items = Column(Integer, default = None)

	channel_id = Column(Integer, ForeignKey('channel.id'))
	channel = relationship("Channel", back_populates="playlists")

	videos = relationship("Video", secondary = video_playlist_table)

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.create_all(engine)
