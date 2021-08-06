from time import sleep
from pytube import Search
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Go to spotify for developers, make a new app and enter your client ID, client Secret and redirect url below.
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_url = 'YOUR_REDIRECT_URI'

scopes = 'playlist-modify-public'
playlist_uri = input("Paste playlist uri from spotify: ")


spotify_auth = SpotifyOAuth(client_id, client_secret, redirect_url, scope=scopes)

sp = spotipy.Spotify(auth_manager=spotify_auth)
playlist = sp.playlist(playlist_uri)
playlist_tracks = playlist['tracks']
playlist_title = playlist['name']
playlist_track_titles = []
choose_track = input("Do you want to choose from options for each track in playlist %s? y/n: "%playlist_title)
total_tracks = 0
for i, item in enumerate(playlist_tracks['items']):
    playlist_track_titles.append(item['track'])
    total_tracks += 1
#download songs from youtube
track_number = 0
for track in playlist_track_titles:
    track_number += 1
    search_term = track['name'] + ' by ' + track['artists'][0]['name']
    print("Searching for :", search_term)
    search_term = search_term.lower()
    yt_search = Search(search_term)

    while True:
        try:
            results = yt_search.results
            # if they want to choose which track, show options, else choose first option
            if choose_track.lower().strip() == 'y':
                for i, video in enumerate(results):
                    try:
                        #video.check_availability()
                        print("Track",i,":", video.title)
                    except:
                        print(video.title, "is unavailable")
                track_index = int(input("Which track should be downloaded? (-1 for more results): "))
                if track_index == -1:
                    try:
                        yt_search.get_next_results()
                    except:
                        print("Unable to get next results")
                    continue
            else:
                track_index = 0
                # filter out super long versions
                for i in range(len(results)):
                    title = results[i].title.lower()
                    if title.find('hours') != -1 or title.find('extended') != -1:
                        track_index += 1
                    else:
                        break
            vid = results[track_index]
            skip_download = False
            break
        except:
            try:
                yt_search.get_next_results()
            except:
                print("Unable to find results for :", search_term)
                skip_download = True
                break
    if not skip_download:
        aud = vid.streams.filter(only_audio=True).get_audio_only()
        if aud:
            print("Downloading",track_number,"of", total_tracks,":", vid.title)
            aud.download(output_path="./"+playlist_title)
            print("Finished downloading: ", vid.title)
        else:
            print("Unable to download audio from video: ", vid.title)
print("Finished downloading all tracks")
