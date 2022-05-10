from xml.sax.handler import feature_external_ges
from pyparsing import col
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re 
import pandas as pd

with open("secret.txt") as f:
        secret_ls = f.readlines()
        cid = str(secret_ls[0])
        secret = str(secret_ls[1])
cid="879ddc6c44d54b92926465b1894ebea0"
secret="****************************"#put secret here


def ari_to_features(ari):
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    #Audio features
    features = sp.audio_features(ari)[0]
    
    #Artist of the track, for genres and popularity
    artist = sp.track(ari)["artists"][0]["id"]
    artist_pop = sp.artist(artist)["popularity"]
    artist_genres = sp.artist(artist)["genres"]
    artist_name=sp.artist(artist)["name"]
    #Track popularity
    track_pop = sp.track(ari)["popularity"]
    track_name = sp.track(ari)["name"]

    
    #Add in extra features
    features["artist_name"] = artist_name
    features["track_name"] = track_name
    features["artist_pop"] = artist_pop
    if artist_genres:
        features["genres"] = " ".join([re.sub(' ','_',i) for i in artist_genres])
    else:
        features["genres"] = "unknown"
    features["track_pop"] = track_pop
    features=pd.DataFrame([features])
    
    return features





