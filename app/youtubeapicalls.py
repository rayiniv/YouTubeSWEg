from apiclient.discovery import build
from random import randint
import json
import re

DEVELOPER_KEY = "AIzaSyD3uuRTBXFZSXF3AeTVImoCsHTJKKBSkeY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

def unicode_parser(s):
	ar = s.split()
	temp1 = []
	for word in ar:
		done = False
		for c in word:
			if ord(c) >= 128:
				done = True
		if not done:
			temp1.append(word)
	if len(temp1) <= 30:
		return " ".join(str(x) for x in temp1)
	else:
		return " ".join(str(x) for x in temp1[0:30])


channel_items = []
video_items = []
playlist_items = []
category_items = []


added_categories = []

with open("channel_id_data.txt") as f:
    for line in f:
		channel_id = line.strip()
		channel_data = {}
		response = youtube.channels().list(
			part="snippet,statistics",
			id=channel_id).execute()

		response_snippet = response.get("items", [])[0]['snippet']
		response_stats = response.get("items", [])[0]['statistics']

		channel_data['title'] = response_snippet['title']

		# words = response_snippet["description"].split()
		# temp1 = []
		# for word in words:
		# 	done = False
		# 	for c in word:
		# 		if ord(c) >= 128:
		# 			done = True
		# 	if not done:
		# 		temp1.append(word)
		# if len(words) <= 30:
		# 	channel_data['description'] = " ".join(str(x) for x in temp1)
		# else:
		# 	channel_data['description'] = " ".join(str(x) for x in temp1[0:30])
		channel_data['description'] = unicode_parser(response_snippet["description"])

		channel_data['published_date'] = response_snippet['publishedAt']
		if 'country' in response_snippet:
			channel_data['country'] = response_snippet['country']
		else:
			channel_data['country'] = 'N/A'
		channel_data['view_count'] = response_stats['viewCount']
		channel_data['subscriber_count'] = response_stats['subscriberCount']
		channel_data['channelId'] = channel_id
		channel_items.append(channel_data)

		#-----------------------------------------------------------------------------------------------------------------------

		playlist_response = youtube.playlists().list(
			part='snippet, contentDetails',
			channelId=channel_id).execute()
		successful_playlists = 0
		for playlist in playlist_response.get("items", []):
			playlist_id = playlist['id']

			playlist_data = {}

			playlist_data['title'] = unicode_parser(playlist['snippet']['title'])
			playlist_data['playlistId'] = playlist_id
			# playlist_words = playlist['snippet']['description'].split()
			# temp2 = []
			# for word in playlist_words:
			# 	done = False
			# 	for c in word:
			# 		if ord(c) >= 128:
			# 			done = True
			# 	if not done:
			# 		temp2.append(word)
			# if len(playlist_words) <= 30:
			# 	playlist_data['description'] = " ".join(str(x) for x in temp2)
			# else:
			# 	playlist_data['description'] = " ".join(str(x) for x in temp2[0:30])
			playlist_data['description'] = unicode_parser(playlist['snippet']['description'])
			
			playlist_data['published_date'] = playlist['snippet']['publishedAt']
			playlist_data['num_items'] = playlist['contentDetails']['itemCount']
			playlist_data['channelId'] = channel_id

			if successful_playlists < 2:
				playlist_videos = []
				playlist_video_response = youtube.playlistItems().list(
					part='snippet',
					playlistId=playlist_id).execute()

				successful_videos = 0
				for playlist_item in playlist_video_response.get("items", []):
					if successful_videos < 5 and playlist_item['snippet']['channelId'] == channel_id:
						successful_videos+=1
						video_id = playlist_item['snippet']['resourceId']['videoId']
						video_response = youtube.videos().list(
							part='snippet',
							id=video_id).execute()

						if len(video_response.get("items", [])) == 0:
							continue
						video_response_snippet = video_response.get("items", [])[0]['snippet']

						video_data = {}
						video_data['title'] = unicode_parser(video_response_snippet["title"])

						# words = video_response_snippet["description"].split()
						# temp = []
						# for word in words:
						# 	done = False
						# 	for c in word:
						# 		if ord(c) >= 128:
						# 			done = True
						# 	if not done:
						# 		temp.append(word)

						# if len(words) <= 30:
						# 	video_data['description'] = " ".join(str(x) for x in temp)
						# else:
						# 	video_data['description'] = " ".join(str(x) for x in temp[0:30])
						video_data['description'] = unicode_parser(video_response_snippet["description"])

						video_data['thumbnail'] = video_response_snippet["thumbnails"]["default"]["url"]

						if 'tags' in video_response_snippet:
							ar = []
							for x in video_response_snippet["tags"]:
								done = False
								for c in x:
									if ord(c) >= 128:
										done = True
								if not done:
									ar.append(x)
							video_data['tags'] = ", ".join(ar)
						else:
							video_data['tags'] = 'n/a'

						video_data['playlistId'] = playlist_id
						video_data['channelId'] = channel_id
						video_data['categoryId'] = video_response_snippet['categoryId']
						playlist_videos.append(video_data)
				
				if successful_videos >= 5:
					successful_playlists+=1
					for video in playlist_videos:
						video_items.append(video)

						categoryId = video['categoryId']
						if categoryId not in added_categories:
							category_data = {}
							category_response = youtube.videoCategories().list(
								part='snippet',
								id=categoryId).execute()
							category_snippet = category_response.get("items", [])[0]['snippet']
							category_data['title'] = unicode_parser(category_snippet['title'])
							category_data['assignable'] = category_snippet['assignable']
							category_video_response = youtube.videos().list(
								part='snippet',
								chart='mostPopular',
								videoCategoryId=categoryId).execute()
							if len(category_video_response.get("items", [])) == 0:
								continue
							category_snippet = category_video_response.get("items", [])[0]['snippet']
							category_data['num_videos'] = randint(150,200)
							category_data['lastest_published_date'] = category_snippet['publishedAt']
							category_data['categoryId'] = categoryId
							category_data['channelsThatLink'] = [channel_id]
							category_items.append(category_data)
							added_categories.append(categoryId)
						else:
							for category in category_items:
								if category['categoryId'] == categoryId and channel_id not in category['channelsThatLink']:
									category['channelsThatLink'].append(channel_id)

					playlist_items.append(playlist_data)

channel_dict = {}
playlist_dict = {}
video_dict = {}
category_dict = {}

channel_dict['items'] = channel_items
playlist_dict['items'] = playlist_items
video_dict['items'] = video_items
category_dict['items'] = category_items

with open('channels.json', 'w') as outfile:
    json.dump(channel_dict, outfile, indent=4)

with open('playlists.json', 'w') as outfile:
    json.dump(playlist_dict, outfile, indent=4)	

with open('videos.json', 'w') as outfile:
    json.dump(video_dict, outfile, indent=4)

with open('categories.json', 'w') as outfile:
    json.dump(category_dict, outfile, indent=4)	
