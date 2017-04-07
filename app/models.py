# pylint: disable = invalid-name
# pylint: disable = missing-docstring
# pylint: disable = import-error
# pylint: disable = too-few-public-methods
# pylint: disable = pointless-string-statement

from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import os

Base = declarative_base()

video_category_table = Table('video_category', Base.metadata,
                             Column('categories_id', Integer,
                                    ForeignKey('category.id')),
                             Column('videos_id', Integer,
                                    ForeignKey('video.id')))

video_playlist_table = Table('video_playlist', Base.metadata,
                             Column('playlists_id', Integer,
                                    ForeignKey('playlist.id')),
                             Column('videos_id', Integer,
                                    ForeignKey('video.id')))

channel_category_table = Table('channel_category', Base.metadata,
                               Column('categories_id', Integer,
                                      ForeignKey('category.id')),
                               Column('channels_id', Integer,
                                      ForeignKey('channel.id')))


class Video(Base):
    """
    Model for a video.
    Contains attributes for a video.
    Linked to channel
    Linked to category
    """
    __tablename__ = "video"
    id = Column(Integer, primary_key=True)

    title = Column(String(750), nullable=False)
    description = Column(String(750), nullable=False)
    thumbnail = Column(String(750), nullable=False)
    tags = Column(String(750), nullable=False)
    video_url = Column(String(750), nullable=False)

    channel_id = Column(Integer, ForeignKey('channel.id'))
    channel = relationship("Channel", back_populates="videos")

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates="videos")


class Channel(Base):
    """
    Model for a channel.
    Contains attributes for a channel.
    Linked to videos
    Linked to playlists
    """
    __tablename__ = "channel"
    id = Column(Integer, primary_key=True)

    title = Column(String(750), nullable=False)
    description = Column(String(750), nullable=False)
    published_date = Column(DateTime, default=None)
    country = Column(String(750), nullable=False)
    view_count = Column(BigInteger, nullable=False)
    subscriber_count = Column(BigInteger, nullable=False)

    videos = relationship("Video", back_populates="channel")
    playlists = relationship("Playlist", back_populates="channel")


class Category(Base):
    """
    Model for a cateogry.
    Contains attributes for a category.
    Linked to videos
    Linked to channels
    """
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)

    title = Column(String(750), nullable=False)
    latest_published_date = Column(DateTime, default=None)
    num_videos = Column(Integer, nullable=False)
    assignable = Column(Boolean, unique=False, default=True)

    videos = relationship("Video", back_populates="category")

    channels = relationship("Channel", secondary=channel_category_table)


class Playlist(Base):
    """
    Model for a playlist.
    Contains attributes for a playlist.
    Linked to channel
    Linked to videos
    """
    __tablename__ = "playlist"
    id = Column(Integer, primary_key=True)

    title = Column(String(750), nullable=False)
    description = Column(String(750), nullable=False)
    published_date = Column(DateTime, default=None)
    num_items = Column(Integer, default=None)

    channel_id = Column(Integer, ForeignKey('channel.id'))
    channel = relationship("Channel", back_populates="playlists")

    videos = relationship("Video", secondary=video_playlist_table)

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
Base.metadata.create_all(engine)
