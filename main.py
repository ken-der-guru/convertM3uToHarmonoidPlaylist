"""Copyright (C) 2023 anonymous
This program is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not,
see <https://www.gnu.org/licenses/>."""

import pathlib
import time
import logging
import sys
import json

import eyed3

logger = logging.getLogger(__name__)
# Set logging level
logger.setLevel(logging.DEBUG)  # remove newline at end of line

formatter = logging.Formatter("%(message)s ")

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

# Initialize m3u_path as Path() -> while loop works
m3u_path = pathlib.Path()
# wait till a valid Path to .m3u playlist was supplied
while m3u_path.is_file() is False:
    m3u_path = pathlib.Path(input('enter valid URI to m3u Playlist:\n'))

# Format of playlists in the Harmonoid Playlist.JSON file 
# playlistDictHarmonoid = [{'name': None,
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


# m3u specification:
# https://en.wikipedia.org/wiki/M3U

with open(m3u_path) as f:
    tracks = []
    playlistTitle = ' '
    for i, line in enumerate(f):
        line = line.replace('\n', '')  # remove newline at end of line
        if '#PLAYLIST' in line:
            playlistTitle = line.replace('#PLAYLIST', '')  # set title of playlist

        if '#' in line:  # '#' indicates that the line is a comment or additional unnecessary info -> skip line
            continue
        if '/' in line:  # '/' indicates that the line is a Path to a song
            path = pathlib.Path(line)

            audiofile = eyed3.load(path.absolute())  # open the file with eyed3 to read its metadata

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
# If there was no title in .m3u file set it to the name of the .m3u file
if playlistTitle == '':
    playlistTitle = m3u_path.name[0:m3u_path.name.rfind('.m3u')]

logger.info(f"Title of Playlist: '{playlistTitle}'")
playlistDictHarmonoid = {'name': playlistTitle,
                         'id': 3,
                         'tracks': tracks, }
# print(playlistDictHarmonoid)

# print(json.dumps(playlistDictHarmonoid, indent=4))

harmonoidPlaylist_path = pathlib.Path.joinpath(pathlib.Path.home(), '.Harmonoid', 'Playlists.JSON')

answer = str.lower(input(f"Is this the path to your Harmonoid Playlists.JSON file?\n'{harmonoidPlaylist_path}'\n["
                         f"yes/no]?\n"))
while answer != 'yes' and answer != 'y' and answer != 'no' and answer != 'n':
    logger.debug(f'answer: {answer}')
    answer = str.lower(input('[yes/no]?\n'))
if answer == 'no' or answer == 'n':
    harmonoidPlaylist_path = pathlib.Path(input('enter valid Path to your Harmonoid Playlists.JSON file:\n'))
    while harmonoidPlaylist_path.is_file() is False:
        harmonoidPlaylist_path = pathlib.Path(input('enter valid Path to your Harmonoid Playlists.JSON file:\n'))

# determine the count of playlists to insert the .m3u playlist at the end
with open(harmonoidPlaylist_path) as f:
    data = json.load(f)
    r = -2
    for line in data['playlists']:
        i = line.get('id', None)
        if i > r:
            r = i

    logger.debug(f"largest Playlist id: {r}")
    playlistDictHarmonoid = {'name': m3u_path.name[0:m3u_path.name.rfind('.m3u')],
                             'id': r + 1,
                             'tracks': tracks, }
    oldPlaylist = data['playlists']
    newPlaylist = oldPlaylist.append(playlistDictHarmonoid)
    playlistNewHarmonoid = {"playlists": newPlaylist}
    # print(json.dumps(playlistNewHarmonoid, indent=4))

# write the updated Playlist.JSON file
with open(harmonoidPlaylist_path, 'w') as f:
    f.write(json.dumps(playlistNewHarmonoid, indent=4))
    print('Added playlist to Harmonoid')
