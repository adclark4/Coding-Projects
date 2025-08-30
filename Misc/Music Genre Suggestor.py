# Music Genre Suggestor
#
# This program suggests a music genre based on the user's mood. The user
# is prompted to input their mood, and the program then suggests a genre
# that matches the mood. The program uses a predefined list of mood-genre
# mappings and provides the user with a suggestion for their listening pleasure.
#
# Features:
# - The program matches common moods (e.g., happy, sad, energetic) to specific music genres.
# - The user can enter different moods, and the program will suggest an appropriate genre.
# - The suggestion is based on mood associations that are commonly linked to specific genres.
#
# Requirements:
# - The user must provide a mood in text form that corresponds to the predefined moods in the program.
#
# Author: Anthony "AJ" Clark

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Define your Spotify API credentials
client_id = 'client id'  # Replace with your actual Client ID
client_secret = 'cleint secret'  # Replace with your actual Client Secret

# Set up Spotify client credentials manager
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Define a function to suggest a music genre based on mood
def suggest_genre(mood):
    mood_to_genre = {
        'happy': 'pop',
        'sad': 'blues',
        'energetic': 'electronic',
        'relaxed': 'jazz',
        'romantic': 'r&b',
        'angry': 'metal'
    }
    return mood_to_genre.get(mood.lower(), 'pop')  # Default to 'pop' if mood is not found


# Define a function to get Spotify track details for a genre
def get_spotify_link(genre):
    results = sp.search(q=genre, type='track', limit=1)

    # Check if 'tracks' key exists and if it contains any items
    if 'tracks' in results and results['tracks']['items']:
        track_info = results['tracks']['items'][0]

        # Prepare a dictionary with track details
        track_details = {
            'name': track_info['name'],  # Track name
            'artist': track_info['artists'][0]['name'],  # First artist's name
            'album': track_info['album']['name'],  # Album name
            'release_date': track_info['album']['release_date'],  # Release date of the album
            'spotify_url': track_info['external_urls']['spotify']  # Spotify link to the track
        }
        return track_details

    # Return message if no track is found
    else:
        return {"error": "No track found for this genre."}


# Main function
def main():
    # Ask the user for their mood
    mood = input("What's your mood? (e.g., happy, sad, energetic, relaxed, romantic, angry): ")

    # Suggest a genre based on mood
    genre = suggest_genre(mood)
    print(f"Suggested genre for mood '{mood}': {genre}")

    # Get the Spotify link for a track in the suggested genre
    track_info = get_spotify_link(genre)

    # Display the track information
    if "error" in track_info:
        print(track_info["error"])
    else:
        print(f"Track Name: {track_info['name']}")
        print(f"Artist: {track_info['artist']}")
        print(f"Album: {track_info['album']}")
        print(f"Release Date: {track_info['release_date']}")
        print(f"Spotify URL: {track_info['spotify_url']}")


# Run the main function
if __name__ == "__main__":
    main()
