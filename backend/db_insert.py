from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from db_create import Base, video_category_table, video_playlist_table, channel_category_table, Video, Channel, Category, Playlist
 
engine = create_engine('sqlite:///youtubesweg.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
new_video = Video(title = "video title", description = "video description", thumbnail = "video thumbnail", tags = "video tags")
new_channel = Channel(title = "channel title", description = "channel description", country = "channel country", view_count = 10, subscriber_count = 10)
new_category = Category(title = "category title", num_videos = 10, assignable = False)
new_playlist = Playlist(title = "playlist title", description = "playlist description", tags = "playlist tags", num_items = 10)

# Link channel to video
new_video.channel = new_channel
# Link category to video
new_video.categories.append(new_category)

# Link video to channel
new_channel.videos.append(new_video)
# Link playlist to channel
new_channel.playlists.append(new_playlist)

# Link video to category
new_category.videos.append(new_video)
# Link channel to category
new_category.channels.append(new_channel)

# Link channel to playlist
new_playlist.channel = new_channel
# Link video to playlist
new_playlist.videos.append(new_video)

# Add video, channel, category, and playlist to their respective tables
session.add(new_video)
session.add(new_channel)
session.add(new_category)
session.add(new_playlist)

# Commit all changes to DB
session.commit()
