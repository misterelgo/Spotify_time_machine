import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

travel_year = input("What year would you want to travel to? YYYY-MM-DD")

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
url = f"https://www.billboard.com/charts/hot-100/{travel_year}"
print(url)
r = requests.get(url, headers=header)
print(r.status_code)

soup = BeautifulSoup(r.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
print(song_names)

#Spotify API Authorization credentials
Client_ID = "2cb01ccd674a438b9a1c30e208cdc64b"
Client_Secret = "46a0a57c64794c09b1fe87907503ed34"
Redirect_URI = "http://example.com"

#Spotify authentification
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID,
                                               client_secret=Client_Secret,
                                               redirect_uri=Redirect_URI,
                                               scope="playlist-modify-private"))
user_id = sp.current_user()["id"]
# Search Spotify for the Songs from Step 1
year = travel_year.split("-")[0]
song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating and Adding to Spotify Playlist
#name "YYYY-MM-DD Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name=f"{travel_year} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)