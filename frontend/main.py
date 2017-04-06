# pylint: disable = bad-whitespace
# pylint: disable = invalid-name
# pylint: disable = missing-docstring
# pylint: disable = global-statement
# pylint: disable = import-error
import logging
import os
import socket
import datetime
import sys

sys.path.append('../app/')

from models import Video, Channel, Category, Playlist, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy
import json

app = Flask(__name__)

# Environment variables are defined in app.yaml.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

def to_arr_dict(objs):
    result = []
    for obj in objs:
        curr_dict = {}
        attrs = [a for a in dir(obj) if not a.startswith('_') and not a == "metadata"
          and not a == "channel" and not a == "category" and not a == "videos" 
          and not a == "playlists" and not a == "channels"]

        for attr in attrs:
            if attr == "published_date" or attr == "latest_published_date":
                curr_dict[attr] = getattr(obj, attr).strftime("%B %d, %Y")
            else:
                curr_dict[attr] = getattr(obj, attr)
        result.append(curr_dict)
    return result

def video_to_dict(objs):
    result = []
    for obj in objs:
        curr_dict = {}
        attrs = [a for a in dir(obj) if not a.startswith('_') and not a == "metadata"
          and not a == "channel" and not a == "category"]

        for attr in attrs:
            curr_dict[attr] = getattr(obj, attr)

        curr_dict["channel_title"] = obj.channel.title
        curr_dict["category_title"] = obj.category.title

        result.append(curr_dict)
    return result    

def category_to_dict(objs):
    result = []
    for obj in objs:
        curr_dict = {}
        attrs = [a for a in dir(obj) if not a.startswith('_') and not a == "metadata"
          and not a == "channel" and not a == "category" and not a == "videos" 
          and not a == "playlists" and not a == "channels"]

        for attr in attrs:
            if attr == "published_date" or attr == "latest_published_date":
                curr_dict[attr] = getattr(obj, attr).strftime("%B %d, %Y")
            elif attr == "assignable":
                curr_dict[attr] = str(getattr(obj, attr))
            else:
                curr_dict[attr] = getattr(obj, attr)
        curr_dict["most_popular_video"] = obj.videos[0].title
        curr_dict["most_popular_video_id"] = obj.videos[0].id

        curr_dict["most_popular_channel"] = obj.channels[0].title
        curr_dict["most_popular_channel_id"] = obj.channels[0].id

        result.append(curr_dict)
    return result     

def playlist_to_dict(objs):
    result = []
    for i, obj in enumerate(objs):
        curr_dict = {}
        attrs = [a for a in dir(obj) if not a.startswith('_') and not a == "metadata"
          and not a == "channel" and not a == "category" and not a == "videos" 
          and not a == "playlists" and not a == "channels"]

        for attr in attrs:
            if attr == "published_date" or attr == "latest_published_date":
                curr_dict[attr] = getattr(obj, attr).strftime("%B %d, %Y")
            else:
                curr_dict[attr] = getattr(obj, attr)
        if curr_dict['description'] == '':
            if i%2==0:
                curr_dict['description'] = obj.channel.description
            else:
                curr_dict['description'] = obj.videos[0].description              
        result.append(curr_dict)
    return result    

num_per_page = 6


video_all = session.query(Video).all()
channel_all = session.query(Channel).all()
category_all = session.query(Category).all()
playlist_all = session.query(Playlist).all()

videos = video_to_dict(video_all)
channels = to_arr_dict(channel_all)
categories = category_to_dict(category_all)
playlists = playlist_to_dict(playlist_all)

@app.route('/db_testing')
def db_testing():
    engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    output = ""
    for video in session.query(Video).all():
        output += video.video_url + "<br />"
    return output

@app.route('/')
def splash_page():
    return render_template('splash_page.html')

@app.route('/video')
def video():
    return render_template('video_tab.html')

@app.route('/channel')
def channel():
    return render_template('channel_tab.html')

@app.route('/category')
def category():
    return render_template('category_tab.html')

@app.route('/playlist')
def playlist():
    return render_template('playlist_tab.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

@app.route('/video/<num>')
def video_instance(num):
    video_obj = None
    for video in video_all:
        if video.id == int(num):
            video_obj = video
            break

    kwargs = {'headers': ['Title', 'Channel', 'Description', 'Thumbnail', 'Tags', 'Categories'],
              'url': 'https://www.youtube.com/embed/' + video_obj.video_url,
              'vid_title': video_obj.title,
              'title_url': '/video/' + num,
              'channel': video_obj.channel.title,
              'channel_url': '/channel/' + str(video_obj.channel.id),
              'description': video_obj.description,
              'thumbnail': video_obj.thumbnail,
              'tags': video_obj.tags,
              'category': video_obj.category.title,
              'category_url': '/category/' + str(video_obj.category.id)}
    return render_template('video.html', **kwargs)


@app.route('/channel/<num>')
def channel_instance(num):
    channel_obj = None
    for channel in channel_all:
        if channel.id == int(num):
            channel_obj = channel
            break

    video_array = []
    for video in channel_obj.videos:
        curr_dict = {}
        curr_dict['video_title'] = video.title
        curr_dict['video_url'] = '/video/' + str(video.id)
        video_array.append(curr_dict)

    playlist_array = []
    for playlist in channel_obj.playlists:
        curr_dict = {}
        curr_dict['playlist_title'] = playlist.title
        curr_dict['playlist_url'] = '/playlist/' + str(playlist.id)
        playlist_array.append(curr_dict)


    kwargs = {'headers': ['Title', 'Description', 'Date of Publication', 'Country', 'View Count', 'Subscriber Count'],
              'channel_title': channel_obj.title,
              'channel_url': '/channel/' + num,
              'description': channel_obj.description,
              'date_of_publication': channel.published_date.strftime("%B %d, %Y"),
              'country': channel_obj.country,
              'view_count': channel_obj.view_count,
              'subscriber_count': channel_obj.subscriber_count,
              'video_array': video_array,
              'playlist_array': playlist_array}

    return render_template('channel.html', **kwargs)

@app.route('/category/<num>')
def category_instance(num):
    category_obj = None
    for category in category_all:
        if category.id == int(num):
            category_obj = category
            break

    video_array = []
    for video in category_obj.videos:
        curr_dict = {}
        curr_dict['video_title'] = video.title
        curr_dict['video_url'] = '/video/' + str(video.id)
        video_array.append(curr_dict)

    channel_array = []
    for channel in category_obj.channels:
        curr_dict = {}
        curr_dict['channel_title'] = channel.title
        curr_dict['channel_url'] = '/channel/' + str(channel.id)
        channel_array.append(curr_dict)


    kwargs = {'headers': ['Title', 'Latest Published Video Date', 'Number of Videos', 'Assignable', 'Most Popular Video', 'Most Popular Channel'],
              'category_title': category_obj.title,
              'category_url': '/category/' + num,
              'latest_published_video_date': category_obj.latest_published_date.strftime("%B %d, %Y"),
              'num_videos': category_obj.num_videos,
              'assignable': str(category_obj.assignable),
              'most_popular_video': [category_obj.videos[0].title, '/video/' + str(category_obj.videos[0].id)],
              'most_popular_channel': [category_obj.channels[0].title, '/channel/' + str(category_obj.channels[0].id)],
              'video_array': video_array,
              'channel_array': channel_array}

    return render_template('category.html', **kwargs)

@app.route('/playlist/<num>')
def playlist_instance(num):
    playlist_obj = None
    for playlist in playlist_all:
        if playlist.id == int(num):
            playlist_obj = playlist
            break

    video_array = []
    for video in playlist_obj.videos:
        curr_dict = {}
        curr_dict['video_title'] = video.title
        curr_dict['video_url'] = '/video/' + str(video.id)
        video_array.append(curr_dict)

    playlist_desc = playlist_obj.description
    if playlist_desc == '':
      if playlist_obj.id % 2 != 0:
        playlist_desc = playlist_obj.channel.description
      else:
        playlist_desc = playlist_obj.videos[0].description

    kwargs = {'headers': ['Title', 'Description', 'Date of Publication', 'Item Count', 'Channel'],
              'playlist_title': playlist_obj.title,
              'playlist_url': '/playlist/' + num,
              'description': playlist_desc,
              'date_of_publication': playlist_obj.published_date.strftime("%B %d, %Y"),
              'item_count': str(playlist_obj.num_items),
              'playlist_channel': [playlist_obj.channel.title, '/channel/' + str(playlist_obj.channel.id)],
              'video_array': video_array}

    return render_template('playlist.html', **kwargs)

# API CALLS
@app.route('/pagination/video/<page_num>')
def video_pagination(page_num):
  starting_num = (int(page_num) - 1) * 9;
  if starting_num + 9 <= len(videos):
    return json.dumps(videos[starting_num:starting_num + 9])
  else:
    return json.dumps(videos[starting_num:])

@app.route('/pagination/channel/<page_num>')
def channel_pagination(page_num):
  starting_num = (int(page_num) - 1) * num_per_page;
  if starting_num + num_per_page <= len(channels):
    return json.dumps(channels[starting_num:starting_num + 6])
  else:
    return json.dumps(channels[starting_num:]) 

@app.route('/pagination/category/<page_num>')
def category_pagination(page_num):
  starting_num = (int(page_num) - 1) * num_per_page;
  if starting_num + num_per_page <= len(categories):
    return json.dumps(categories[starting_num:starting_num + 6])
  else:
    return json.dumps(categories[starting_num:])

@app.route('/pagination/playlist/<page_num>')
def playlist_pagination(page_num):
  starting_num = (int(page_num) - 1) * num_per_page;
  if starting_num + num_per_page <= len(playlists):
    return json.dumps(playlists[starting_num:starting_num + 6])
  else:
    return json.dumps(playlists[starting_num:])    

# @app.route('/sorting/video/<')
# def video_pagination(page_num):
#   starting_num = (int(page_num) - 1) * num_per_page;
#   if starting_num + num_per_page <= len(videos):
#     return json.dumps(videos[starting_num:starting_num + 6])
#   else:
#     return json.dumps(videos[starting_num:])


# @app.route('/pagination/channel/<page_num>')
# def channel_pagination(page_num):
#   starting_num = (int(page_num) - 1) * num_per_page;
#   if starting_num + num_per_page <= len(channels):
#     return json.dumps(videos[starting_num:starting_num + 6])
#   else:
#     return json.dumps(videos[starting_num:])

# @app.route('/pagination/category/<page_num>')
# def category_pagination(page_num):
#   starting_num = (int(page_num) - 1) * num_per_page;
#   if starting_num + num_per_page <= len(categories):
#     return json.dumps(videos[starting_num:starting_num + 6])
#   else:
#     return json.dumps(videos[starting_num:])

# @app.route('/pagination/playlist/<page_num>')
# def playlist_pagination(page_num):
#   starting_num = (int(page_num) - 1) * num_per_page;
#   if starting_num + num_per_page <= len(playlists):
#     return json.dumps(videos[starting_num:starting_num + 6])
#   else:
#     return json.dumps(videos[starting_num:])            

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.' + e)
    return 'An internal error occurred.', 500
    
# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)