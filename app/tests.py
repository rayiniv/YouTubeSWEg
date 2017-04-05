# pylint: disable = invalid-name
# pylint: disable = missing-docstring
# pylint: disable = import-error
# pylint: disable = deprecated-method

from unittest import main, TestCase
from models import Video, Channel, Category, Playlist, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

os.path.prepend('../app/')
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
        self.assertEquals(num_videos, 1)

    def test_video_query_2(self):
        video = session.query(Video).first()
        video_title = video.title
        self.assertEquals(video_title, 'video title')

    def test_video_query_3(self):
        video = session.query(Video).first()
        video_desc = video.description
        self.assertEquals(video_desc, 'video description')

    #--------------
    # Channel Query
    #--------------

    def test_channel_query_1(self):
        channels = session.query(Channel).all()
        num_channels = len(channels)
        self.assertEquals(num_channels, 1)

    def test_channel_query_2(self):
        channel = session.query(Channel).first()
        channel_title = channel.title
        self.assertEquals(channel_title, 'channel title')

    def test_channel_query_3(self):
        channel = session.query(Channel).first()
        channel_desc = channel.description
        self.assertEquals(channel_desc, 'channel description')

    #--------------
    # Category Query
    #--------------

    def test_category_query_1(self):
        categories = session.query(Category).all()
        num_categories = len(categories)
        self.assertEquals(num_categories, 1)

    def test_category_query_2(self):
        category = session.query(Category).first()
        category_title = category.title
        self.assertEquals(category_title, 'category title')

    def test_category_query_3(self):
        category = session.query(Category).first()
        category_num_videos = category.num_videos
        self.assertEquals(category_num_videos, 10)

    def test_category_query_4(self):
        category = session.query(Category).first()
        category_assignable = category.assignable
        self.assertEquals(category_assignable, False)

    #--------------
    # PLaylist Query
    #--------------

    def test_playlist_query_1(self):
        playlists = session.query(Playlist).all()
        num_playlists = len(playlists)
        self.assertEquals(num_playlists, 1)

    def test_playlist_query_2(self):
        playlist = session.query(Playlist).first()
        playlist_title = playlist.title
        self.assertEquals(playlist_title, 'playlist title')

    def test_playlist_query_3(self):
        playlist = session.query(Playlist).first()
        playlist_desc = playlist.description
        self.assertEquals(playlist_desc, 'playlist description')

    def test_playlist_query_4(self):
        playlist = session.query(Playlist).first()
        playlist_tags = playlist.tags
        self.assertEquals(playlist_tags, 'playlist tags')

    def test_playlist_query_5(self):
        playlist = session.query(Playlist).first()
        playlist_num_items = playlist.num_items
        self.assertEquals(playlist_num_items, 10)


if __name__ == "__main__":
    main()
