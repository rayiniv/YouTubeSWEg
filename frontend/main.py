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
            curr_dict[attr] = getattr(obj, attr)
        result.append(curr_dict)
    return result

num_per_page = 6
videos = to_arr_dict(session.query(Video).all())
channels = to_arr_dict(session.query(Channel).all())
categories = to_arr_dict(session.query(Category).all())
playlists = to_arr_dict(session.query(Playlist).all())

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

# @app.route('/channel')
# def channel():
#     return render_template('model.html', title="Channels", table_headers=channel_headers,
#                            data=channels)

# @app.route('/category')
# def category():
#     return render_template('model.html', title="Categories", table_headers=category_headers,
#                            data=categories)

# @app.route('/playlist')
# def playlist():
#     return render_template('model.html', title="Playlists", table_headers=playlist_headers,
#                            data=playlists)

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/video/<num>')
# def video_instance(num):
#     return render_template('video.html', headers=video_headers,
#                            video_link=video_links[int(num) - 1], video_data=videos[int(num) - 1])

# @app.route('/channel/<num>')
# def channel_instance(num):
#     index = int(num) - 1
#     kwargs = {'headers': channel_headers,
#               'channel_video_list': channel_video_list[index],
#               'channel_playlist_list': channel_playlist_list[index],
#               'channel_data': channels[index]}
#     return render_template('channel.html', **kwargs)
#     # return render_template('channel.html', headers=channel_headers,
#     # channel_video_list=channel_video_list[int(num) - 1],    
#     # channel_playlist_list=channel_playlist_list[int(num) - 1],
#     # channel_data=channels[int(num) - 1])

# @app.route('/category/<num>')
# def category_instance(num):
#     index = int(num) - 1
#     kwargs = {'headers': category_headers,
#               'category_video_list': category_video_list[index],
#               'category_channel_list': category_channel_list[index],
#               'category_data': categories[index]}
#     return render_template('category.html', **kwargs)
#     # return render_template('category.html', headers=category_headers,
#     # category_data=categories[int(num) - 1])

# @app.route('/playlist/<num>')
# def playlist_instance(num):
#     index = int(num) - 1
#     kwargs = {'headers': playlist_headers,
#               'playlist_video_list': playlist_video_list[index],
#               'playlist_channel': playlist_channel_list[index],
#               'playlist_data': playlists[index]}
#     return render_template('playlist.html', **kwargs)
#     # return render_template('playlist.html', headers=playlist_headers,
#     # playlist_data=playlists[int(num) - 1])

# API CALLS
@app.route('/pagination/video/<page_num>')
def video_pagination(page_num):
  starting_num = (int(page_num) - 1) * num_per_page;
  if starting_num + num_per_page <= len(videos):
    return json.dumps(videos[starting_num:starting_num + 6])
  else:
    return json.dumps(videos[starting_num:])

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.' + e)
    return 'An internal error occurred.', 500
    
# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)