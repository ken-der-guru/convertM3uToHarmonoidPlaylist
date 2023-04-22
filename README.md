# convertM3uToHarmonoidPlaylist
___

Application to import .m3u Playlists in the [Harmonoid](https://github.com/harmonoid/harmonoid) music player.

**Why?**\
Because this functionality is sadly not a Harmonoid feature at the time.

**How it works:**
1. Run main.py 
2. Enter path to a playlist, in the m3u file format, which should get imported to harmonoid
3. App reads the file and extracts the URIs of the songs from the playlist
4. App extracts the title of the playlist (after #PLAYLIST), if none was found it uses the filename of the .m3u playlist
5. eyed3 is used to extract the id3 tags of the songs
6. Open the Playlist.JSON file and insert the playlist in a format harmonoid can understand. Then save the new file.
7. Restart Harmonoid
8. Finish!

**Dependencies:**
- [eyed3](https://eyed3.readthedocs.io/en/latest/)