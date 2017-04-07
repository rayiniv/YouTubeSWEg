# pylint: disable = invalid-name
# pylint: disable = missing-docstring
# pylint: disable = import-error
# pylint: disable = deprecated-method

from unittest import main, TestCase
from models import Video, Channel, Category, Playlist, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()


class TestYoutubesweg(TestCase):

    #------------
    # Video Query
    #------------

    def test_video_query_1(self):
        videos = session.query(Video).all()
        num_videos = len(videos)
        self.assertEquals(num_videos, 200)

    def test_video_query_2(self):
        video = session.query(Video).first()
        video_title = video.title
        self.assertEquals(video_title, 'Boomer: Between the Games Week 17')

    def test_video_query_3(self):
        video = session.query(Video).first()
        video_channel = video.channel.title
        self.assertEquals(video_channel, 'CBS Local Sports')

    #--------------
    # Channel Query
    #--------------

    def test_channel_query_1(self):
        channels = session.query(Channel).all()
        num_channels = len(channels)
        self.assertEquals(num_channels, 22)

    def test_channel_query_2(self):
        channel = session.query(Channel).first()
        channel_title = channel.title
        self.assertEquals(channel_title, 'CBS Local Sports')

    def test_channel_query_3(self):
        channel = session.query(Channel).first()
        channel_desc = channel.description
        result = channel_desc.startswith("CBS")
        self.assertEquals(True, result)

    #--------------
    # Category Query
    #--------------
    def test_category_query_1(self):
        categories = session.query(Category).all()
        num_categories = len(categories)
        self.assertEquals(num_categories, 9)

    def test_category_query_2(self):
        category = session.query(Category).first()
        category_title = category.title
        self.assertEquals(category_title, 'Sports')

    def test_category_query_3(self):
        category = session.query(Category).first()
        category_num_videos = category.num_videos
        self.assertEquals(category_num_videos, 186)

    def test_category_query_4(self):
        category = session.query(Category).first()
        category_assignable = category.assignable
        self.assertEquals(category_assignable, True)

    #--------------
    # PLaylist Query
    #--------------

    def test_playlist_query_1(self):
        playlists = session.query(Playlist).all()
        num_playlists = len(playlists)
        self.assertEquals(num_playlists, 40)

    def test_playlist_query_2(self):
        playlist = session.query(Playlist).first()
        playlist_title = playlist.title
        self.assertEquals(playlist_title, 'The 2017 Masters Tournament on ESPN')

    def test_playlist_query_3(self):
        playlist = session.query(Playlist).first()
        playlist_desc = playlist.description
        result = playlist_desc.startswith("The best")
        self.assertEquals(True, result)


    def test_playlist_query_4(self):
        playlist = session.query(Playlist).first()
        playlist_num_items = playlist.num_items
        self.assertEquals(playlist_num_items, 9)


if __name__ == "__main__":
    main()
