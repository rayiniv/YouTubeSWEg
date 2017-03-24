# pylint: disable = bad-whitespace
# pylint: disable = invalid-name
# pylint: disable = missing-docstring
# pylint: disable = global-statement
# pylint: disable = import-error

import logging

from flask import Flask, render_template

app = Flask(__name__)

video_links = [
    "https://www.youtube.com/embed/SpXw0qiy3Wo?list=PLC1uUM4twa8gQwnAQuwTl17lfzDYElmAn",
    "https://www.youtube.com/embed/zEyEC34MY1A?list=PL36E7A2B75028A3D6",
    "https://www.youtube.com/embed/Fi37_GYRYCs?list=PLn3nHXu50t5zJPLQFFNGFSHhnsc-xpsnR"]

video_headers = ["Title", "Channel", "Description",
                 "Thumbnail", "Tags", "Categories"]

video1 = [
    ("21 Savage & Metro Boomin - X ft Future (Official Music Video)", "/video/1"),
    ("21 Savage", "/channel/1"),
    "21 Savage & Metro Boomin deliver a visual for their platinum selling record, 'X' featuring"
    + " Future",
    "https://i.ytimg.com/vi/SpXw0qiy3Wo/hqdefault.jpg?custom=true&w=120&h=90&jpg444=true&jpgq=90&sp"
    + "=68&sigh=DLoxY9SpDoeNH4L0n58Rgl-_Sog",
    "21 savage x, x 21 savage, 21 savage future x, x 21 savage future, 21 savage metro boomin x",
    ("Music", "/category/1")]
video2 = [
    ("Python Lists", "/video/2"),
    ("Khan Academy", "/channel/2"),
    "Understanding the basics of lists in Python",
    "https://i.ytimg.com/vi/zEyEC34MY1A/hqdefault.jpg?custom=true&w=120&h=90&jpg444=true&jpgq=90&sp"
    + "=68&sigh=rM9BoXNJo2Gwx6Z_bt08X5s6xWw",
    "khan academy, academy khan, khan, academy, python, sal, lists",
    ("Education", "/category/2")]
video3 = [
    ("A Dog's Remarkable Journey To Find A Home | SC Featured", "/video/3"),
    ("ESPN", "/channel/3"),
    "A distance of 6,455 miles doesn't begin to measure the journey one dog named Arthur made to"
    + " join a team and find a family.",
    "https://i.ytimg.com/vi/Fi37_GYRYCs/hqdefault.jpg?custom=true&w=120&h=90&jpg444=true&jpgq=90&sp"
    + "=68&sigh=qij2LjwL7tKV70TUjNw0pTKY3Jg (4KB)",
    "arthur the dog, arthur, arthur sc featured, arthur dog espn feature, sportscenter feature dog,"
    + " dog remarkable journey",
    ("Sports", "/category/3")]

videos = [video1, video2, video3]


channel_headers = ["Title", "Description", "Date of Publication",
                   "Country", "View Count", "Subscriber Count"]

channel1 = [
    ("21 Savage", "/channel/1"),
    "21 Savage's official channel! Subscribe for all music videos, behind the scenes and tour" +
    " videos from 21 as they'll drop here first.",
    "Feb 8, 2014",
    "United States",
    "319,281,006",
    "734,993"]

channel1_videos = [
    ("21 Savage & Metro Boomin - X ft Future (Official Music Video)", "/video/1")]
channel1_playlists = [("21 Savage | Music Videos", "/playlist/1")]

channel2 = [
    ("Khan Academy", "/channel/2"),
    "Our mission to provide a world-class education for anyone, anywhere. All Khan Academy" +
    " content is available for free at www.khanacademy.org.",
    "Nov 16, 2006",
    "United States",
    "1,072,136,706",
    "3,059,083"]

channel2_videos = [("Python Lists", "/video/2")]
channel2_playlists = [("Computer Science", "/playlist/2")]

channel3 = [
    ("ESPN", "/channel/3"),
    "ESPN on YouTube features the best of shows like SportsCenter, SC6, and First Take, along" +
    " with the most surprising and inspiring stories in sports. Get all your sports videos," +
    " sports information, sports news, sports scores, and sports analysis right here.",
    "Oct 31, 2005",
    "United States",
    "5,369,132",
    "1,657,655"]

channel3_videos = [
    ("A Dog's Remarkable Journey To Find A Home | SC Featured", "/video/3")]
channel3_playlists = [("ESPN Originals", "/playlist/3")]

channel_video_list = [channel1_videos, channel2_videos, channel3_videos]
channel_playlist_list = [channel1_playlists,
                         channel2_playlists, channel3_playlists]

channels = [channel1, channel2, channel3]


category_headers = ["Title", "Latest Published Video Date", "Number of videos",
                    "Assignable", "Most popular video", "Most popular channel"]

category1 = [
    ("Music", "/category/1"),
    "March 20, 2017",
    "200",
    "true",
    ("21 Savage & Metro Boomin - X ft Future (Official Music Video)", "/video/1"),
    ("21 Savage", "/channel/1")]

category1_videos = [
    ("21 Savage & Metro Boomin - X ft Future (Official Music Video)", "/video/1")]
category1_channels = [("21 Savage", "/channel/1")]

category2 = [
    ("Education", "/category/2"),
    "March 19, 2017",
    "174",
    "true",
    ("Python Lists", "/video/2"),
    ("Khan Academy", "/channel/2")]

category2_videos = [("Python Lists", "/video/2")]
category2_channels = [("Khan Academy", "/channel/2")]

category3 = [
    ("Sports", "/category/3"),
    "March 20, 2017",
    "190",
    "true",
    ("A Dog's Remarkable Journey To Find A Home | SC Featured", "/video/3"),
    ("ESPN", "/channel/3")]

category3_videos = [
    ("A Dog's Remarkable Journey To Find A Home | SC Featured", "/video/3")]
category3_channels = [("ESPN", "/channel/3")]


category_video_list = [category1_videos, category2_videos, category3_videos]
category_channel_list = [category1_channels,
                         category2_channels, category3_channels]

categories = [category1, category2, category3]


playlist_headers = ["Title", "Description",
                    "Associated Tags", "Date of Publication", "Item Count"]

playlist1 = [
    ("21 Savage | Music Videos", "/playlist/1"),
    "Music videos by 21 Savage. Various directors. All music can be found here: " +
    "http://www.livemixtapes.com/main.php?artist=21+savage",
    "video, sharing, camera phone, video phone, free, upload",
    "Dec 25, 2016",
    "14"]

playlist1_channel = ("21 Savage", "/channel/1")
playlist1_videos = [
    ("21 Savage & Metro Boomin - X ft Future (Official Music Video)", "/video/1")]

playlist2 = [
    ("Computer Science", "/playlist/2"),
    "Introduction to programming and computer science",
    "khan academy, academy khan, computer science, academy, khan",
    "Jul 2, 2014",
    "23"]

playlist2_channel = ("Khan Academy", "/channel/2")
playlist2_videos = [("Python Lists", "/video/2")]

playlist3 = [
    ("ESPN Originals", "/playlist/3"),
    "From '30 For 30' to 'SC Featured,'' these are ESPN's original videos telling some of the" +
    " greatest stories that transcend sports.",
    "arthur the dog, arthur, arthur sc featured, arthur dog espn feature, sportscenter feature" +
    " dog, dog remarkable journey, arthur journey, dog traveled espn, art",
    "Mar 9 2017",
    "15"]

playlist3_channel = ("ESPN", "/channel/3")
playlist3_videos = [
    ("A Dog's Remarkable Journey To Find A Home | SC Featured", "/video/3")]


playlist_channel_list = [playlist1_channel,
                         playlist2_channel, playlist3_channel]
playlist_video_list = [playlist1_videos, playlist2_videos, playlist3_videos]

playlists = [playlist1, playlist2, playlist3]


@app.route('/')
def splash_page():
    return render_template('splash_page.html')


@app.route('/video')
def video():
    return render_template('model.html', title="Videos", table_headers=video_headers, data=videos)


@app.route('/channel')
def channel():
    return render_template('model.html', title="Channels", table_headers=channel_headers,
                           data=channels)


@app.route('/category')
def category():
    return render_template('model.html', title="Categories", table_headers=category_headers,
                           data=categories)


@app.route('/playlist')
def playlist():
    return render_template('model.html', title="Playlists", table_headers=playlist_headers,
                           data=playlists)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    return render_template('test.html', title='test', table_headers=playlist_headers, data=playlists)    


@app.route('/video/<num>')
def video_instance(num):
    return render_template('video.html', headers=video_headers,
                           video_link=video_links[int(num) - 1], video_data=videos[int(num) - 1])


@app.route('/channel/<num>')
def channel_instance(num):
    index = int(num) - 1
    kwargs = {'headers': channel_headers,
              'channel_video_list': channel_video_list[index],
              'channel_playlist_list': channel_playlist_list[index],
              'channel_data': channels[index]}
    return render_template('channel.html', **kwargs)
    # return render_template('channel.html', headers=channel_headers,
    # channel_video_list=channel_video_list[int(num) - 1],
    # channel_playlist_list=channel_playlist_list[int(num) - 1],
    # channel_data=channels[int(num) - 1])


@app.route('/category/<num>')
def category_instance(num):
    index = int(num) - 1
    kwargs = {'headers': category_headers,
              'category_video_list': category_video_list[index],
              'category_channel_list': category_channel_list[index],
              'category_data': categories[index]}
    return render_template('category.html', **kwargs)
    # return render_template('category.html', headers=category_headers,
    # category_data=categories[int(num) - 1])


@app.route('/playlist/<num>')
def playlist_instance(num):
    index = int(num) - 1
    kwargs = {'headers': playlist_headers,
              'playlist_video_list': playlist_video_list[index],
              'playlist_channel': playlist_channel_list[index],
              'playlist_data': playlists[index]}
    return render_template('playlist.html', **kwargs)
    # return render_template('playlist.html', headers=playlist_headers,
    # playlist_data=playlists[int(num) - 1])


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.' + e)
    return 'An internal error occurred.', 500

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
