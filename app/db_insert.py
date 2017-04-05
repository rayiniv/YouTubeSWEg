# pylint: disable = import-error
# pylint: disable = invalid-name
# pylint: disable = missing-docstring

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Video, Channel, Category, Playlist

import os

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

new_video = Video(title="video title", description="video description",
                  thumbnail="video thumbnail", tags="video tags")
new_channel = Channel(title="channel title", description="channel description",
                      country="channel country", view_count=10, subscriber_count=10)
new_category = Category(title="category title",
                        num_videos=10, assignable=False)
new_playlist = Playlist(title="playlist title",
                        description="playlist description", num_items=10)

# Link channel to video
new_video.channel = new_channel #DONE
# Link category to video
new_video.category = new_category #DONE

# Link video to channel
new_channel.videos.append(new_video) #DONE
# Link playlist to channel
new_channel.playlists.append(new_playlist) #DONE

# Link video to category
new_category.videos.append(new_video) #DONE
# Link channel to category
new_category.channels.append(new_channel) #DONE

# Link channel to playlist
new_playlist.channel = new_channel #DONE
# Link video to playlist
new_playlist.videos.append(new_video) #DONE

# Add video, channel, category, and playlist to their respective tables
session.add(new_video)
session.add(new_channel)
session.add(new_category)
session.add(new_playlist)

# Commit all changes to DB
session.commit()
