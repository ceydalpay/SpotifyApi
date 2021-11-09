import requests
import base64
import datetime
from urllib.parse import urlencode
import json
import sys
import pypyodbc as odbc
from src.authentication import SpotifyAPI


client_id = 'a0b3781c37af438f812c07ef3e338905'
client_secret = '3eaa6aa6f38e4c4e87bc5cb09c7678db'

client = SpotifyAPI(client_id, client_secret)

data = client.get_playlist("5hg53KxzqRRqFG2MuzoN3P?si=dd7be795b8ab42d4")
tracks = []
audio_feat = []
track = []

DRIVER = 'SQL Server' #will remain same
SERVER_NAME = 'LAPTOP-MFCSV23V\SQLEXPRESS' #your username
DATABASE_NAME = 'SpotifyDatas' #your database name

conn_string = f"""
    Driver={{{DRIVER}}};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trust_Connection=yes;
"""

try:
    conn = odbc.connect(conn_string)
except Exception as e:
    print(e)
    print("Task is terminated")
    sys.exit()
else:
    cursor = conn.cursor()

insert_track_statement = """
    INSERT INTO Tracks
    VALUES (?, ?, ?, ?, ?)
"""

insert_feature_statement = """
    INSERT INTO Audio_Features
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

trackRecords = []
featureRecords = []
playlist_id=[]


for i in data["tracks"]["items"]:
    tracks.append(i["track"]["id"])

for i in range(0, len(tracks)):
    track.append(client.get_track(tracks[i]))
    audio_feat.append(client.get_audio_features(tracks[i]))
for i in x["items"]:
    playlist_id.append(i["id"])

for i in range(0, len(playlist_id)):
    playlist_id.append(client.get_playlist(playlist_id[i]))

for j in range(0, len(playlist_id)):
    for i in a[j]["tracks"]["items"]:
        tracks.append(i["track"]["id"])

for i in range(0, len(audio_feat)):
    featureRecords.append([audio_feat[i].get("id"), audio_feat[i].get("danceability"), audio_feat[i].get("energy"),
                  audio_feat[i].get("key"), audio_feat[i].get("loudness"), audio_feat[i].get("mode"),
                  audio_feat[i].get("speechiness"),
                  audio_feat[i].get("acousticness"), audio_feat[i].get("instrumentalness"),
                  audio_feat[i].get("liveness"),
                  audio_feat[i].get("valence"), audio_feat[i].get("tempo"), audio_feat[i].get("duration_ms")]),

    trackRecords.append([track[i].get("id"), track[i].get("name"), track[i].get("artists")[0].get("name"), track[i].get("album").get("name"), 1])

try:
    for tracks in trackRecords:
        cursor.execute(insert_track_statement, tracks)

    for audioFeature in featureRecords:
        cursor.execute(insert_feature_statement, audioFeature)

except Exception as e:
    cursor.rollback()
    print(e.value)
    print("transaction rolled back")
else:
    print("audio features inserted successfully")
    cursor.commit()
finally:
    if conn.connected == 1:
        print("connection is closed")
        conn.close()
