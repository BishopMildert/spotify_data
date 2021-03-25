#! /usr/bin/python3
import os
import spotipy
import pandas as pd
import datetime
import time
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

# API Credentials
API_PUBLIC = os.environ.get('CLIENT_ID')
API_SECRET = os.environ.get('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(API_PUBLIC, API_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids


ids = getTrackIDs('spotify',
                  '37i9dQZEVXcJiDfIvmU4zA')

# print(len(ids))


def getTrackFeats(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # features
    feats = features[0]
    acousticness = feats['acousticness']
    danceability = feats['danceability']
    energy = feats['energy']
    instrumentalness = feats['instrumentalness']
    liveness = feats['liveness']
    loudness = feats['loudness']
    speechiness = feats['speechiness']
    tempo = feats['tempo']
    time_signature = feats['time_signature']

    track = [name, album, artist, release_date, length, popularity, acousticness, danceability,
             energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]

    return track

# looping over track ids


tracks = []

for i in range(len(ids)):
    # time.sleep(.5)
    track = getTrackFeats(ids[i])
    tracks.append(track)

# creating the dataset
df = pd.DataFrame(tracks, columns=[' name', 'album', 'artist', 'release_date', 'length', 'popularity', 'dancebility',
                                   'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
today_date = str(datetime.date.today())
df[['playlist_date']] = today_date

# saving playlist data to DF
df.to_csv(f'data/{today_date}-playlist.csv')
