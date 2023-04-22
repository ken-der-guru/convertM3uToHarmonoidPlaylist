import os
import pathlib
import time
import eyed3
import logging
import sys
import json

logger = logging.getLogger(__name__)
# Set logging level
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(message)s ")

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)


m3u_path = pathlib.Path()
while m3u_path.is_file() is False:
    m3u_path = pathlib.Path(input('enter valid URI to m3u Playlist:\n'))
# Format of playlists in the Harmonoid Playlist.JSON file 
#playlistDictHarmonoid = [{'name': None,
#                          'id': None,
#                          'tracks': [
#                              {
#                                  "uri": None,
#                                  "trackName": None,
#                                  "albumName": None,
#                                  "trackNumber": 1,
#                                  "discNumber": 1,
#                                  "albumLength": 1,
#                                  "albumArtistName": "Deichkind",
#                                  "trackArtistNames": ["Deichkind"],
#                                  "timeAdded": int(time.time()),
#                                  "duration": 0,
#                                  "bitrate": 0,
#                              }],
#                          }]

with open(m3u_path) as f:
    tracks = []
    for i, line in enumerate(f):
        if '#EXTINF' in line:
            continue
        if '/' in line:
            path = line.replace('\n', '')
            path = pathlib.Path(path)
            audiofile = eyed3.load(path)
            logger.debug(audiofile.tag.track_num[0])
            # TODO print(audiofile.tag.track_num[0])
            try:
                artists = [audiofile.tag.artist]
            except AttributeError:
                pass
            tracks.append({
                "uri": path.absolute().as_uri(),
                "trackName": audiofile.tag.title,
                "albumName": audiofile.tag.album,
                "trackNumber": 1,
                "discNumber": 1,
                "albumLength": 1,
                "albumArtistName": audiofile.tag.album_artist,
                "trackArtistNames": artists,
                "timeAdded": int(time.time()),
                "duration": 0,
                "bitrate": 0
            })

logger.debug(tracks)
logger.info(f"Title of Playlist: '{m3u_path.name[0:m3u_path.name.rfind('.m3u')]}'")
playlistDictHarmonoid = {'name': m3u_path.name[0:m3u_path.name.rfind('.m3u')],
                         'id': 3,
                         'tracks': tracks, }
# print(playlistDictHarmonoid)

#print(json.dumps(playlistDictHarmonoid, indent=4))

harmonoidPlaylist_path = os.path.join(pathlib.Path.home(), '.Harmonoid', 'Playlists.JSON')
answer = input(f"Is this the path to your Harmonoid Playlists.JSON file?\n'{harmonoidPlaylist_path}'\n[yes/no]?\n")
while answer != 'yes' and answer != 'no':
    logger.debug(f'answer: {answer}')
    answer = input('[yes/no]?\n')
if answer == 'no':
    harmonoidPlaylist_path = pathlib.Path(input('enter valid Path to your Harmonoid Playlists.JSON file:\n'))
    while harmonoidPlaylist_path.is_file() is False:
        harmonoidPlaylist_path = pathlib.Path(input('enter valid Path to your Harmonoid Playlists.JSON file:\n'))



f = None
with open(harmonoidPlaylist_path) as f:
    data = json.load(f)
    r = -2
    for line in data['playlists']:
        i = line.get('id', None)
        if i > r:
            r = i

    logger.debug(f"largest Playlist id: {r}")
    playlistDictHarmonoid = {'name': m3u_path.name[0:m3u_path.name.rfind('.m3u')],
                             'id': r+1,
                             'tracks': tracks, }
    s = data['playlists']
    s.append(playlistDictHarmonoid)
    playlistNewHarmonoid = {"playlists": s}
    #print(json.dumps(playlistNewHarmonoid, indent=4))
with open(harmonoidPlaylist_path, 'w') as f:
    f.write(json.dumps(playlistNewHarmonoid, indent=4))
    print('Added playlist to Harmonoid')
