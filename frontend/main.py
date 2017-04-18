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
import operator 
import math
import copy

sys.path.append('../app/')

from models import Video, Channel, Category, Playlist, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy
import json

import subprocess

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

def channel_to_dict(objs):
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

        video_arr = []
        for video in obj.videos:
          video_arr.append(video.id)
        curr_dict["videos"] = video_arr

        playlist_arr = []
        for playlist in obj.playlists:
          playlist_arr.append(playlist.id)
        curr_dict["playlists"] = playlist_arr

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

        channel_arr = []
        for channel in obj.channels:
          channel_arr.append(channel.id)
        curr_dict["channels"] = channel_arr

        video_arr = []
        for video in obj.videos:
          video_arr.append(video.id)
        curr_dict["videos"] = video_arr

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

        video_arr = []
        for video in obj.videos:
          video_arr.append(video.id)
        curr_dict["videos"] = video_arr

        result.append(curr_dict)
    return result    

num_per_page = 6

video_all = session.query(Video).all()
channel_all = session.query(Channel).all()
category_all = session.query(Category).all()
playlist_all = session.query(Playlist).all()

videos = video_to_dict(video_all)
channels = channel_to_dict(channel_all)
categories = category_to_dict(category_all)
playlists = playlist_to_dict(playlist_all)

videos_copy = list(videos)
channels_copy = list(channels)
categories_copy = list(categories)
playlists_copy = list(playlists)

search_results = []

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

@app.route('/about')
def about():
    return render_template('about_tab.html')

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


@app.route('/search/<query>')
def search(query):
  queries = query.lower().split(' ')
  global search_results
  search_results = []
  union_list = []
  single_list = []

  copy_of_videos = copy.deepcopy(videos)

  for video in copy_of_videos:
    check_all = []
    for key, value in video.items():
      for q in queries:
        if q in str(value).lower():
          app.logger.warning(str(key))
          video[key] = str(value).lower().replace(q, "<mark>" + q + "</mark>")
          if q not in check_all:
            check_all.append(q)

    if len(check_all) == len(queries):
      union_list.append(video)
    elif len(check_all) > 0:
      single_list.append(video)





  copy_of_channels = copy.deepcopy(channels)

  for channel in copy_of_channels:
    check_all = []
    for key, value in channel.items():
      for q in queries:
        if q in str(value).lower():
          app.logger.warning(str(key))
          channel[key] = str(value).lower().replace(q, "<mark>" + q + "</mark>")
          if q not in check_all:
            check_all.append(q)

    if len(check_all) == len(queries):
      union_list.append(channel)
    elif len(check_all) > 0:
      single_list.append(channel)




  copy_of_playlists = copy.deepcopy(playlists)

  for playlist in copy_of_playlists:
    check_all = []
    for key, value in playlist.items():
      for q in queries:
        if q in str(value).lower():
          playlist[key] = str(value).lower().replace(q, "<mark>" + q + "</mark>")
          if q not in check_all:
            check_all.append(q)

    if len(check_all) == len(queries):
      union_list.append(playlist)
    elif len(check_all) > 0:
      single_list.append(playlist)




  copy_of_categories = copy.deepcopy(categories)

  for category in copy_of_categories:
    check_all = []
    for key, value in category.items():
      for q in queries:
        if q in str(value).lower():
          category[key] = str(value).lower().replace(q, "<mark>" + q + "</mark>")
          if q not in check_all:
            check_all.append(q)

    if len(check_all) == len(queries):
      union_list.append(category)
    elif len(check_all) > 0:
      single_list.append(category)            


  for u in union_list:
    search_results.append(u)

  for s in single_list:
    search_results.append(s)

  if len(search_results) == 0:
    search_results.append([-1])

  return render_template('search.html', total_pages=math.ceil(len(search_results) / 9.0), query=query)

@app.route('/pagination/search/<page_num>')
def search_pagination(page_num):
  starting_num = (int(page_num) - 1) * 9;
  if starting_num + 9 <= len(search_results):
    return json.dumps(search_results[starting_num:starting_num + 9])
  else:
    return json.dumps(search_results[starting_num:])

# API CALLS
@app.route('/pagination/video/<page_num>')
def video_pagination(page_num):
  starting_num = (int(page_num) - 1) * 9;
  if starting_num + 9 <= len(videos_copy):
    return json.dumps(videos_copy[starting_num:starting_num + 9])
  else:
    return json.dumps(videos_copy[starting_num:])

@app.route('/pagination/channel/<page_num>')
def channel_pagination(page_num):
  starting_num = (int(page_num) - 1) * num_per_page;
  if starting_num + num_per_page <= len(channels_copy):
    return json.dumps(channels_copy[starting_num:starting_num + 6])
  else:
    return json.dumps(channels_copy[starting_num:]) 

@app.route('/pagination/category/<page_num>')
def category_pagination(page_num):
  starting_num = (int(page_num) - 1) * num_per_page;
  if starting_num + num_per_page <= len(categories_copy):
    return json.dumps(categories_copy[starting_num:starting_num + 6])
  else:
    return json.dumps(categories_copy[starting_num:])

@app.route('/pagination/playlist/<page_num>')
def playlist_pagination(page_num):
  starting_num = (int(page_num) - 1) * num_per_page;
  if starting_num + num_per_page <= len(playlists_copy):
    return json.dumps(playlists_copy[starting_num:starting_num + 6])
  else:
    return json.dumps(playlists_copy[starting_num:])    

def sort_results(dict_list, attr_name, reverse):
  new_list = list(dict_list)

  # for item in dict_list:
  #   print(getattr(item, attr_name))


  new_list.sort(key=operator.itemgetter(attr_name))
  if reverse:
    new_list.reverse()
  return new_list

def filter_results(dict_list, attr_name, value):
  new_list = []
  for d in dict_list:
    if d[attr_name] == value:
      new_list.append(d)
  return new_list

@app.route('/sorting/video/<num>/<option>/<filter_channel>/<filter_category>')
def video_sorting(num, option, filter_channel, filter_category):
  global videos_copy
  videos_copy = list(videos)

  if filter_channel != "blank":
    filterChannelOptions = filter_channel.split(",")
    final_results = []
    for opt in filterChannelOptions:
      if opt != "":
        temp = filter_results(videos_copy, "channel_title", opt)
        for dictionary in temp:
          final_results.append(dictionary)
    videos_copy = list(final_results)

  if filter_category != "blank":
    filterCategoryOptions = filter_category.split(",")
    final_results = []
    for opt in filterCategoryOptions:
      if opt != "":
        temp = filter_results(videos_copy, "category_title", opt)
        for dictionary in temp:
          final_results.append(dictionary)
    videos_copy = list(final_results)

  if filter_channel != "blank" and filter_category != "blank" and len(videos_copy) == 0:
    videos_copy.append([-1])     
  else:
    if option != "blank":
      if int(num) == 0:
        videos_copy = list(videos_copy)  
      elif int(num) == 1:
        videos_copy = sort_results(videos_copy, option, False)
      else:
        videos_copy = sort_results(videos_copy, option, True)

  return str(videos_copy)

@app.route('/sorting/channel/<num>/<option>/<filter_country>/<filter_none>')
def channel_sorting(num, option, filter_country, filter_none):
  global channels_copy
  channels_copy = list(channels)

  if filter_country != "blank":
    filterCountryOptions = filter_country.split(",")
    final_results = []
    for opt in filterCountryOptions:
      if opt != "":
        temp = filter_results(channels_copy, "country", opt)
        for dictionary in temp:
          final_results.append(dictionary)
    channels_copy = list(final_results)

  if filter_none != "blank":
    filterCategoryOptions = filter_category.split(",")
    final_results = []
    for opt in filterCategoryOptions:
      if opt != "":
        temp = filter_results(videos_copy, "category_title", opt)
        for dictionary in temp:
          final_results.append(dictionary)
    videos_copy = list(final_results)

  if option != "blank":
    if int(num) == 0:
      channels_copy = list(channels_copy)  
    elif int(num) == 1:
      channels_copy = sort_results(channels_copy, option, False)
    else:
      channels_copy = sort_results(channels_copy, option, True)

  return str(channels_copy)     

@app.route('/sorting/category/<num>/<option>/<filter_channel>/<filter_none>')
def category_sorting(num, option, filter_channel, filter_none):
  global categories_copy
  categories_copy = list(categories)

  if filter_channel != "blank":
    filterChannelOptions = filter_channel.split(",")
    final_results = []
    for opt in filterChannelOptions:
      if opt != "":
        temp = filter_results(categories_copy, "most_popular_channel", opt)
        for dictionary in temp:
          final_results.append(dictionary)
    categories_copy = list(final_results)

  if filter_none != "blank":
    filterCategoryOptions = filter_category.split(",")
    final_results = []
    for opt in filterCategoryOptions:
      if opt != "":
        temp = filter_results(videos_copy, "category_title", opt)
        for dictionary in temp:
          final_results.append(dictionary)
    videos_copy = list(final_results)

  if option != "blank":
    if int(num) == 0:
      categories_copy = list(categories_copy)  
    elif int(num) == 1:
      categories_copy = sort_results(categories_copy, option, False)
    else:
      categories_copy = sort_results(categories_copy, option, True)

  return str(categories_copy)    

@app.route('/sorting/playlist/<num>/<option>/<filter_none1>/<filter_none2>')
def playlist_sorting(num, option, filter_none1, filter_none2):
  global playlists_copy
  playlists_copy = list(playlists)

  if option != "blank":
    if int(num) == 0:
      playlists_copy = list(playlists_copy)  
    elif int(num) == 1:
      playlists_copy = sort_results(playlists_copy, option, False)
    else:
      playlists_copy = sort_results(playlists_copy, option, True)

  return str(playlists_copy)    


@app.route('/api/video')  
def video_api():
  response = []
  response_inner = {}
  videos_arr = []
  video_id_arg = request.args.get("id")
  channel_id_arg = request.args.get("channel_id")
  category_id_arg = request.args.get("category_id")
  if video_id_arg != None:
    video_ids = video_id_arg.split(',')
    for video in video_all:
      if str(video.id) in video_ids:
        videos_arr.append(video)
  elif channel_id_arg != None:
    channel_ids = channel_id_arg.split(',')
    for video in video_all:
      if str(video.channel.id) in channel_ids:
        videos_arr.append(video)
  elif category_id_arg != None:
    category_ids = category_id_arg.split(',')
    for video in video_all:
      if str(video.category.id) in category_ids:
        videos_arr.append(video)
  else:
    for video in video_all:
      videos_arr.append(video)

  videos_dict_arr = []
  for video in videos_arr:
    for video_dict in videos:
      if video_dict['id'] == video.id:
        videos_dict_arr.append(video_dict)

  response_inner['num_videos'] = len(videos_dict_arr)
  response_inner['videos'] = videos_dict_arr
  response.append(response_inner)
  return json.dumps(response)

@app.route('/api/channel')  
def channel_api():
  response = []
  response_inner = {}
  channel_arr = []
  channel_id_arg = request.args.get("id")
  country_arg = request.args.get("country")
  if channel_id_arg != None:
    channel_ids = channel_id_arg.split(',')
    for channel in channel_all:
      if str(channel.id) in channel_ids:
        channel_arr.append(channel)
  elif country_arg != None:
    countries = country_arg.split(',')
    for channel in channel_all:
      if str(channel.country) in countries:
        channel_arr.append(channel)
  else:
    for channel in channel_all:
      channel_arr.append(channel)

  channel_dict_arr = []
  for channel in channel_arr:
    for channel_dict in channels:
      if channel_dict['id'] == channel.id:
        channel_dict_arr.append(channel_dict)

  response_inner['num_channels'] = len(channel_dict_arr)
  response_inner['channels'] = channel_dict_arr
  response.append(response_inner)
  return json.dumps(response)

@app.route('/api/category')  
def category_api():
  response = []
  response_inner = {}
  categories_arr = []
  category_id_arg = request.args.get("id")
  channel_id_arg = request.args.get("channel_id")
  if category_id_arg != None:
    category_ids = category_id_arg.split(',')
    for category in category_all:
      if str(category.id) in category_ids:
        categories_arr.append(category)
  elif channel_id_arg != None:
    channel_ids = channel_id_arg.split(',')
    for category in category_all:
      for channel in category.channels:
        if str(channel.id) in channel_ids:
          categories_arr.append(category)
          break
  else:
    for category in category_all:
      categories_arr.append(category)

  categories_dict_arr = []
  for category in categories_arr:
    for category_dict in categories:
      if category_dict['id'] == category.id:
        categories_dict_arr.append(category_dict)

  response_inner['num_categories'] = len(categories_dict_arr)
  response_inner['categories'] = categories_dict_arr
  response.append(response_inner)
  return json.dumps(response)

@app.route('/api/playlist')  
def playlist_api():
  response = []
  response_inner = {}
  playlists_arr = []
  playlist_id_arg = request.args.get("id")
  video_id_arg = request.args.get("video_id")
  if playlist_id_arg != None:
    playlist_ids = playlist_id_arg.split(',')
    for playlist in playlist_all:
      if str(playlist.id) in playlist_ids:
        playlists_arr.append(playlist)
  elif video_id_arg != None:
    video_ids = video_id_arg.split(',')
    for playlist in playlist_all:
      for video in playlist.videos:
        if str(video.id) in video_ids:
          playlists_arr.append(playlist)
          break
  else:
    for playlist in playlist_all:
      playlists_arr.append(playlist)

  playlists_dict_arr = []
  for playlist in playlists_arr:
    for playlist_dict in playlists:
      if playlist_dict['id'] == playlist.id:
        playlists_dict_arr.append(playlist_dict)

  response_inner['num_playlists'] = len(playlists_dict_arr)
  response_inner['playlists'] = playlists_dict_arr
  response.append(response_inner)
  return json.dumps(response)

@app.route('/unit_tests')
def unit_tests():
  return open('tests.out').read()


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.' + e)
    return 'An internal error occurred.', 500
    
# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)