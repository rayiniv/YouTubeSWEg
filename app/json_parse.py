import json
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Video, Channel, Category, Playlist

import os

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

channels_dict = {}
categories_dict = {}
playlists_dict = {}
videos_dict = {}

with open("channels.json") as f:
    channels_dict = json.load(f)

with open("categories.json") as f:
    categories_dict = json.load(f)

with open("playlists.json") as f:
    playlists_dict = json.load(f)   

with open("videos.json") as f:
    videos_dict = json.load(f)     

# print(json.dumps(channels_dict, indent=4, sort_keys=True))

channel_objs = []
video_objs = []
playlist_objs = []
category_objs = []
category_ids_done = []
playlist_ids_done = []
for channel in channels_dict['items']:
	new_date = datetime.datetime.strptime(channel['published_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
	new_channel = Channel(title=channel['title'], description=channel['description'], published_date=new_date, 
		country=channel['country'], view_count=int(channel['view_count']), subscriber_count=int(channel['subscriber_count']))

	channel_id = channel['channelId']
	
	for video in videos_dict['items']:
		if video['channelId'] == channel_id:
			new_video = Video(title=video['title'], description=video['description'],
                  thumbnail=video['thumbnail'], tags=video['tags'], video_url=video['videoId'])

			for category in categories_dict['items']:
				if video['categoryId'] == category['categoryId']:
					if category['categoryId'] not in category_ids_done:
						new_date = datetime.datetime.strptime(category['lastest_published_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
						new_category = Category(title=category['title'], latest_published_date=new_date, 
							num_videos=int(category['num_videos']), assignable=bool(category['assignable']))

						new_category.channels.append(new_channel)

						new_video.category = new_category

						category_objs.append(new_category)
						category_ids_done.append(category['categoryId'])
					else:
						for category_object in category_objs:
							if category_object.title == category['title']:
								if new_channel not in category_object.channels:
									category_object.channels.append(new_channel)

			for playlist in playlists_dict['items']:
				if video['playlistId'] == playlist['playlistId']:
					if playlist['playlistId'] not in playlist_ids_done:
						new_date = datetime.datetime.strptime(playlist['published_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
						new_playlist = Playlist(title=playlist['title'], description=playlist['description'], 
							published_date=new_date, num_items=int(playlist['num_items']))

						new_playlist.channel = new_channel
						new_playlist.videos.append(new_video)

						playlist_objs.append(new_playlist)
						playlist_ids_done.append(playlist['playlistId'])
					else:
						for playlist_object in playlist_objs:
							if playlist_object.title == playlist['title'] and playlist_object.num_items == int(playlist['num_items']):
								playlist_object.videos.append(new_video)

			new_video.channel = new_channel

			video_objs.append(new_video)

	channel_objs.append(new_channel)


for channel in channel_objs:
	session.add(channel)

for video in video_objs:
	session.add(video)

for playlist in playlist_objs:
	session.add(playlist)

for category in category_objs:
	session.add(category)

session.commit()

