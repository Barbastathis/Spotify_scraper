import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import sys

# Replace with your Spotify API credentials
CLIENT_ID = ""
CLIENT_SECRET = ""

def scrape_spotify_playlist_as_json(playlist_url, output_file="scraped.json"):
    # Authenticate with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    
    # Extract the playlist ID from the URL
    try:
        playlist_id = playlist_url.split("/")[-1].split("?")[0]
    except IndexError:
        print("Invalid playlist URL format.")
        return
    
    # Fetch playlist details
    try:
        results = sp.playlist(playlist_id)
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching playlist: {e}")
        return

    # Prepare a list to hold all track data
    tracks_data = []

    # Loop through playlist tracks and collect data
    for item in results['tracks']['items']:
        track = item['track']
        track_data = {
            "album_type": track['album']['album_type'],
            "artists": [
                {
                    "external_urls": artist['external_urls'],
                    "href": artist['href'],
                    "id": artist['id'],
                    "name": artist['name'],
                    "type": artist['type'],
                    "uri": artist['uri']
                }
                for artist in track['artists']
            ],
            "available_markets": track['available_markets'],
            "external_urls": track['external_urls'],
            "href": track['href'],
            "id": track['id'],
            "images": track['album']['images'],
            "name": track['name'],
            "release_date": track['album']['release_date'],
            "release_date_precision": track['album']['release_date_precision'],
            "total_tracks": track['album']['total_tracks'],
            "type": track['album']['type'],
            "uri": track['uri']
        }
        tracks_data.append(track_data)
    
    # Save data to a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tracks_data, f, indent=4)
    
    print(f"Playlist scraped successfully! Data saved to {output_file}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <playlist_url>")
    else:
        playlist_url = sys.argv[1]
        scrape_spotify_playlist_as_json(playlist_url)
