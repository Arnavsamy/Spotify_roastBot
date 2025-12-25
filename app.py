import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import google.generativeai as genai  
import streamlit as st
from dotenv import load_dotenv


load_dotenv("keys.env")


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



def extract_playlist_id(url):
    """Extracts the ID from a Spotify URL."""
    match = re.search(r"playlist/([a-zA-Z0-9]+)", url)
    if match:
        return match.group(1)
    return None

def get_playlist_tracks(playlist_id):
    """Fetches track names and artists from Spotify."""
    track_list = []
    try:
        results = sp.playlist_items(playlist_id, limit=50)
        
        for item in results['items']:
            track = item.get('track')
            if track:
                name = track['name']
                artist = track['artists'][0]['name']
                track_list.append(f"{artist} - {name}")
                
        return track_list
    except Exception as e:
        return str(e)

def get_roast(tracks):
    """Sends the track list to Gemini for roasting."""
    
    
    playlist_text = ", ".join(tracks[:40]) 

    model = genai.GenerativeModel('gemini-flash-latest')

    
    prompt = (
        f"You are a snarky, elitist music critic. "
        f"You judge people's taste in music harshly. "
        f"Roast the following playlist. Be funny, rude, and specific about the artists. "
        f"Here is the playlist data: {playlist_text}"
    )

    try:
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to Gemini: {e}"



st.set_page_config(page_title="Gemini RoastBot", page_icon="♊")

st.title("♊ The Gemini RoastBot")
st.write("Paste a public Spotify playlist URL below.")

playlist_url = st.text_input("Playlist URL")

if st.button("Roast This"):
    if not playlist_url:
        st.warning("You need to paste a URL first.")
    else:
        pid = extract_playlist_id(playlist_url)
        
        if not pid:
            st.error("Invalid Spotify URL.")
        else:
            with st.spinner("Gemini is judging your soul..."):
                
                tracks = get_playlist_tracks(pid)
                
                if isinstance(tracks, list):
                    
                    roast = get_roast(tracks)
                    
                    
                    st.success("Roast Generated!")
                    st.markdown(f"### 💀 Verdict:\n{roast}")
                    
                    
                    with st.expander("See the tracks analyzed"):
                        st.write(tracks)
                else:
                    st.error(f"Spotify Error: {tracks}")