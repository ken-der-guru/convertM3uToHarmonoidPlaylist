# [convertM3uToHarmonoidPlaylist](https://github.com/ken-der-guru/convertM3uToHarmonoidPlaylist#convertm3utoharmonoidplaylist)
___

Application to import .m3u Playlists() in the [Harmonoid](https://github.com/harmonoid/harmonoid) music player.

**Why?**\
Because this functionality is sadly not a Harmonoid feature at the time.

**How it works**
1. Download the repository as .zip or use `git clone https://github.com/ken-der-guru/convertM3uToHarmonoidPlaylist`
2. Run the `main.py` file
3. Enter path to a playlist, in the m3u8 file format, which should get imported to harmonoid
4. App reads the file and extracts the paths of the songs from the playlist
5. App extracts the title of the playlist (after #PLAYLIST: in an extended m3u File), if none was found it uses the filename of the .m3u playlist
6. eyed3 is used to extract the id3 tags of the songs, needed for the next step
7. Opens the Playlist.JSON file and inserts the playlist in a format harmonoid can understand. Then saves the new file.
8. Restart Harmonoid
9. Finish!

**Requirements**\
run `pip install -r requirements.txt`\
[eyed3](https://eyed3.readthedocs.io/en/latest/)\
Songs in the playlist need the following ID3 tags to be written: albumartist, title, album\
Confirmed to work in Harmonoid v0.3.8

**License**\
Licensed under [GPL-3.0-or-later](LICENSE.txt)