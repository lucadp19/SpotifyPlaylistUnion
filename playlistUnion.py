import os
import sys
import pprint

import spotipy
import spotipy.util as util

spotipy_client_id = ''
spotipy_client_secret = ''
spotipy_redirect_uri = 'http://localhost/'

def get_tracks_from_playlist(sp, username, playlist_id):
    ''' 
    Given a Spotipy object, an username and a playlist_id
    returns a list of all the track ids in the playlist.
    '''
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = [t['track']['id'] for t in results['items']]

    # results returns 100 tracks at a time
    while results['next']:
        results = sp.next(results)
        tracks.extend([t['track']['id'] for t in results['items']])

    return tracks

def track_not_in_playlist(track_list):
    '''
    Returns a function which, given a track id, returns:
        - true if the track isn't in the playlist
        - false if the track is in the playlist. 
    '''
    return (lambda track_id: (not track_id in track_list))

def divide_chunks(track_list, n):
    '''
    Given a list, it divides it into a list of lists, 
    each of them with a length less or equal to n.
    '''
    for i in range(0, len(track_list), n):
        yield track_list[i:i + n]

def playlist_union(username, destination_playlist, source_playlists):
    '''
    Given username, destination playlist and source playlists, the function
    adds all the songs in the list of source playlists into the destination
    playlist. 
    '''
    # use 'playlist-modify-private' if you also want to modify private playlists
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope,
                                        client_id=spotipy_client_id, 
                                        client_secret=spotipy_client_secret,
                                        redirect_uri=spotipy_redirect_uri)


    if token:
        sp = spotipy.Spotify(auth=token)
        destination_playlist_tracks = get_tracks_from_playlist(sp, username, destination_playlist)

        for playlist in source_playlists:
            tracks = get_tracks_from_playlist(sp, username, playlist)
            # filter only the tracks that aren't already present in the destination playlist
            tracks = list(filter(track_not_in_playlist(destination_playlist_tracks), tracks))
            # spotipy requires that each track id has the 'spotify:track:' prefix
            tracks = ['spotify:track:' + t for t in tracks]

            if tracks:
                # We can add only 100 tracks at a time, so the list of track ids is divided
                # into a list of list, each of them with a length less or equal to 100
                tracks_chunks = divide_chunks(tracks, 100)
                for chunk in tracks_chunks:
                    result = sp.user_playlist_add_tracks(username, destination_playlist, chunk)
                print("Added tracks!")
            else: 
                print("No tracks to add!")
    else:
        print('Could not validate token.')

if __name__ == '__main__':
    if len(sys.argv) > 3:
        username = sys.argv[1]
        destination_playlist = sys.argv[2]
        source_playlists = sys.argv[3:]
    else:
        print("Not enough arguments: you should call this program together " \
                "with: username destination_playlist source_playlists...")
        sys.exit()
    
    playlist_union(username, destination_playlist, source_playlists)
