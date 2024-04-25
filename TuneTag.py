# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 11:24:19 2024

@author: michalk
"""

import discogs_client
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
print(matplotlib.__version__)

def spotify_api(title, artist):
    client_id = '84ee7db5f52140019eacb7d89ea2fb9f'
    client_secret = 'edaa00ed8d55423ba00c96cf97442e2c'
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    name = '%s %s' %(artist, title) 
    result = sp.search(name) 
    song_uri = result['tracks']['items'][0]['uri']
    feat = sp.audio_features(song_uri)[0]
    return feat


def discogs_api(title, artist):
    d = discogs_client.Client('ExampleApplication/0.1', user_token='rNucODWfQpwMuPAqSSGseRVQCnJqwZPKGnfgkWCp')
    results = d.search(title=title, artist=artist, type='release')
    res = results[0]
    
    artist_querry = results[0].artists
    artist = [x.name for x in artist_querry] 
    return res

def url_tag(url):
    return f'<a href ="{url}"><img src="https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png" width=50></a>'

def camelot_tranversion(mode, key):
    df = pd.DataFrame({
        'num': [8,11,3,6,10,1,5,8,0,3,7,10,2,5,9,0,4,7,11,2,6,9,1,4],
        'mode':[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        'camelot':['1A','1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B','6A', '6B', 
                   '7A', '7B', '8A', '8B', '9A','9B', '10A','10B', '11A', '11B', '12A', '12B'],
        'key': ['A♭ Minor', 'B Major', 'E♭ Minor', 'F# Major', 'B♭ Minor', 'D♭ Major', 'F Minor', 'A♭ Major',
                'C Minor', 'E♭ Major', 'G Minor', 'B♭ Major', 'D Minor', 'F Major', 'A Minor', 'C Major',
                'E Minor', 'G Major', 'B Minor', 'D Major', 'F# Minor', 'A Major', 'D♭ Minor', 'E Major']})
    df = df.loc[(df['mode']==mode) & (df['num'] == key)]
    return (df['camelot'].values[0], df['key'].values[0])


st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {1400}px;
        padding-top: {5}rem;
        padding-right: {5}rem;
        padding-left: {5}rem;
        padding-bottom: {5}rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )



def search_song(title, artist):
    try:
        feat = spotify_api(title, artist)
        res = discogs_api(title, artist)
    
        image = res.images[0]['resource_url']
    
        danceability = feat['danceability']*100
        energy = feat['energy']*100
        instrument = feat['instrumentalness']*100
        acoustic = feat['acousticness']*100
        liveness = feat['liveness']*100
        speech = feat['speechiness']*100
        yt_logo = "https://upload.wikimedia.org/wikipedia/commons/e/e1/Logo_of_YouTube_%282015-2017%29.svg"
        spotify_logo = "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg"
        
        
        key_num = feat['key']
        mode = feat['mode']
        bpm = '%.0f' %feat['tempo']
        duration = res.tracklist[0].duration
      
        camelot, key = camelot_tranversion(mode, key_num)
        try:
            style = ', '.join(res.styles)
        except:
            style='N/A'
        try:
            genre = ', '.join(res.genres)
        except:
            genre='N/A'
        
        remix_name = [x.title for x in res.videos]
        remix_url = [x.url for x in res.videos]
        df_yt = pd.DataFrame({'name': remix_name, 'url':remix_url})
        df_yt['url'] = df_yt['url'].apply(url_tag)
    
        features = [danceability, energy, instrument, acoustic, liveness, speech]
        features_name= ['Danceability', 'Energy', 'Instrumentalness', 'Acousticness', 'Liveness', 'Speechiness']
        fig, ax = plt.subplots(figsize=(18,3))
        ax.axis('off')
        for ind, feature in enumerate(features):
            ax = plt.subplot(1,6, ind+1)
            ax.pie([100-feature, feature], colors=['whitesmoke', 'crimson'], startangle=90, shadow=True, wedgeprops=dict(width=0.2, edgecolor='w'))
            ax.text(0.48,0.48, '%.1f' %feature, transform=ax.transAxes, fontsize=22, ha='center', va='center')
            ax.text(0,-1.5, features_name[ind], ha='center', fontsize=16)
            
        col1, col2 = st.columns([0.2, 0.9])
        with col1:
            st.text('')
            st.text('')
            st.image(image)
            try:
                yt = res.videos[0].url
                spot = feat['uri']
                st.markdown(f'''
                                <table style='border-collapse: collapse;'>
                                <tr><td style='border: 1px solid white;'>
                                <a href="{yt}"><img src="{yt_logo}" width=100, height=50></a></td>
                                <td style='border: 1px solid white;'>
                                <a href="{spot}"><img src="{spotify_logo}" width=50, height=50></a>
                                </td></tr></table>''',unsafe_allow_html=True)
            except:
                None
        
        with col2:
            st.markdown(f'''
            <h1><b>{res.artists_sort} - {res.title}</b></h1>
            <table style='border-collapse: collapse;'>
            <tr><td style='border: 1px solid white;'>
            <table>
            <tr><td style='width: 150px;' bgcolor=#f2ebee><center><h2>{bpm}</center></h2>
            <h6><center>BPM</center></h6>
            </td></tr> 
            </table>
            </td>
            <td style='border: 1px solid white;'>
            <table>
            <tr><td style='width: 150px;' bgcolor=#f2ebee><center><h2>{duration}</center></h2>
            <h6><center>Duration</center></h6>
            </td></tr> 
            </table>
            </td>
            <td style='border: 1px solid white;'>
            <table>
            <tr><td style='width: 150px;' bgcolor=#f2ebee><center><h2>{camelot}</center></h2>
            <h6><center>Camelot</center></h6>
            </td></tr> 
            </table>
            </td>
            <td style='border: 1px solid white;'>
            <table>
            <tr><td style='width: 200px;' bgcolor=#f2ebee><center><h2>{key}</center></h2>
            <h6><center>Key</center></h6>
            </td></tr> 
            </table>
            </td>
            </tr>
            </table>
            <br>
            <table style='border-collapse: collapse;'>
            <tr>
            <td style='border: 1px solid white;'><center><font size="5"><b>Released</b>: <pre>{res.year}</pre></font></center></td>
            <td style='border: 1px solid white;'><center><font size="5"><b>Genre:</b> <pre>{genre}</pre></font></center></td>
            <td style='border: 1px solid white;'><center><font size="5"><b>Style:</b> <pre>{style}</pre></font></center></td>
            </tr>
            </table>
            ''', unsafe_allow_html=True)
        col1, col2 = st.columns([0.8,0.2])
        with col1: 
            st.pyplot(fig)
            #st.markdown(f'''<table border=1><tr><td>{st.pyplot(fig)}</td></tr></table>''') 
            st.markdown(f'''
            <br>
            <h4>Other Versions:</h4>
            <h5>{df_yt.to_html(border=0, header=False, escape=False)}</h5></div>''', unsafe_allow_html=True)
        return res, feat
    except:
       st.warning('There is no artist or song in the database')


    

st.sidebar.header('Navigation')
artist = st.sidebar.text_input('Artist', value='opus')
title = st.sidebar.text_input('Title', value='life is')

if st.sidebar.button("Search"):
    search_song(title, artist)

   





