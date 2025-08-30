# Song Similarity Finder
#
# This program allows the user to input the name and artist of a song,
# then uses the Spotify API to find songs that are similar to the one
# specified. The program retrieves and displays a list of tracks with
# similar characteristics (e.g., genre, tempo, mood) to the input song.
# The user can interact with the program to find and explore new songs
# based on similarity to their favorite tracks.
#
# To run this program, you need to have a Spotify API Client ID and Secret,
# and the 'spotipy' library installed. The program authenticates via the
# Spotify API, searches for similar songs, and displays the names and
# Spotify links to the user.
#
# Author: Anthony "AJ" Clark

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

# Define your Spotify API credentials
client_id = 'f246e453f63d4afdaa7271c05f1fef68'  # Replace with your actual Client ID - NEVER SHARE WITH OTHERS!
client_secret = '6f97369ba7d748ca89a74a7b95089f57'  # Replace with your actual Client Secret - NEVER SHARE WITH OTHERS!

# Set up Spotify client credentials manager
try:
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
except Exception as e:
    print(f"Error setting up Spotify client: {e}")
    sys.exit(1)


def get_similar_songs(track_name, artist_name, limit=10):
    """
    Fetches similar songs based on the given track and artist using Spotify's Recommendations API.

    Parameters:
    - track_name (str): The name of the track.
    - artist_name (str): The name of the artist.
    - limit (int): Number of similar songs to retrieve.

    Returns:
    - list: A list of dictionaries containing similar song details.
    - str: An error message if the track is not found.
    """
    # Create a search query that includes both track and artist
    query = f"track:{track_name} artist:{artist_name}"

    try:
        # Search for the track
        results = sp.search(q=query, type='track', limit=1)
    except Exception as e:
        return f"An error occurred while searching for the track: {e}"

    # Check if any tracks were found
    if results['tracks']['items']:
        track = results['tracks']['items'][0]  # Get the first matching track
        track_id = track['id']

        try:
            # Get recommendations based on the seed track
            recommendations = sp.recommendations(seed_tracks=[track_id], limit=limit)
        except Exception as e:
            return f"An error occurred while fetching recommendations: {e}"

        similar_songs = []
        for rec_track in recommendations['tracks']:
            song_info = {
                'track_name': rec_track['name'],
                'artist': rec_track['artists'][0]['name'],
                'spotify_url': rec_track['external_urls']['spotify']
            }
            similar_songs.append(song_info)

        return similar_songs
    else:
        return f"Track '{track_name}' by '{artist_name}' not found. Please check the spelling and try again."


def main():
    print("=== Spotify Song Similarity Finder ===\n")

    # Prompt user for song name and artist name
    track_name = input("Enter the song name: ").strip()
    artist_name = input("Enter the artist name: ").strip()

    if not track_name or not artist_name:
        print("Both song name and artist name are required.")
        sys.exit(1)

    # Fetch similar songs
    similar_songs = get_similar_songs(track_name, artist_name)

    # Display the results
    if isinstance(similar_songs, list):
        print(f"\nSongs similar to '{track_name}' by {artist_name}:\n")
        for idx, song in enumerate(similar_songs, start=1):
            print(f"{idx}. Track: {song['track_name']}")
            print(f"   Artist: {song['artist']}")
            print(f"   Spotify URL: {song['spotify_url']}\n")
    else:
        # If similar_songs is not a list, it's an error message
        print(similar_songs)


if __name__ == "__main__":
    main()
