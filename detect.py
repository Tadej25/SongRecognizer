import requests
import os
import eyed3 as e
import json
import pathlib

# https://dashboard.audd.io/
song_dir = str(pathlib.Path(__file__).parent.resolve()) + "/songs"
api_token = input("Give me your API token: ")
all_or_new = input("Type 'new' to go through only new songs or 'all' to go throug all songs: ")
new = False
songs = os.listdir(song_dir)
not_found = []
if all_or_new.upper() == "NEW":
    new = True
for idx,song in enumerate(songs):
    sound_file = song_dir + "/" + song
    audiofile = e.load(sound_file)

    if new and audiofile.tag.title != None and audiofile.tag.artist != None and audiofile.tag.album != None:
        print(str(idx + 1) + "/" + str(len(songs)) + "; Skipping " + song + "...")
        continue
    print(str(idx + 1) + "/" + str(len(songs)) + "; Getting data for " + song + "...")

    data = {
        'api_token': api_token,
    }
    files = {
        'file': open(sound_file, 'rb'),
    }
    result = requests.post('https://api.audd.io/', data=data, files=files)
    json_object = json.loads(result.text)
    
    if json_object["status"] != "success":
        print("There seems to be an error with the file; Continuing...")
    else:
        if json_object["result"] != None:
            audiofile.tag.title = u"" + json_object["result"]["title"]
            audiofile.tag.artist = u"" + json_object["result"]["artist"]
            audiofile.tag.album = u"" + json_object["result"]["album"]
            audiofile.tag.save()
            new_file_name = (song_dir + "/" + audiofile.tag.artist +
                            " - " + audiofile.tag.title).replace("/", "")
            print("file: " + song + "; artist: " + audiofile.tag.artist + "; title: " + audiofile.tag.title + "; album: " + audiofile.tag.album + "; new_file_name: " + new_file_name)
        else:
            not_found.append(song)
            print("Could not find file: " + song + "; Continuing...")
print("Done...")
print("Songs that could not be found: ")
print(not_found)
