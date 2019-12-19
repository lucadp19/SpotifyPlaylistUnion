# Spotify Playlist Union

A simple Python script that **adds all the songs** in a list of playlists in a **destination playlist**.

Useful if you have several playlists, for example divided by genre, and you want **a single playlist that contains all the songs you like**.

## Requirements

- Python 3.x
- [Spotipy](https://github.com/plamere/spotipy "Spotipy")
- a Spotify account
- a [Spotify for Developers](https://developer.spotify.com/dashboard/ "Spotify for Developers") account, with a Client ID and Client Secret for this project

## How to use it

- First of all, add your Spotify for Developers' **Client ID** and **Client Secret** to the code.
- Then, if you want to modify your private playlists as well, set the "scope" variable to "**playlist-modify-private**".
- Lastly, call the Python script with the following arguments:
  - **username**
  - **destination playlist ID**
  - **one or more source playlist ID**.
- A playlist ID is a string such as _spotify:playlist:27gN69ebwiJRtXEboL12Ih_. To get it from the desktop app, just click on the three dots and in Share select "c**opy Spotify URI**".
- The first time the app will ask you to log in. After having logged in Spotify, **copy the link the browser redirected you to** and **paste it in the terminal** when asked. 
  - The next times the programm will remember you have logged in, so **it won't ask again** (unless you modify the username or the scope from public to private)!
