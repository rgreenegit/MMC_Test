from typing import List, Optional
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from trie import Trie
import pysolr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

solr_client = pysolr.Solr(
    'http://localhost:8983/solr/autocomplete_core', timeout=10)

with open("data.json") as f:
    music_data = json.load(f)

music_data_trie = Trie()
music_data_trie.build_trie(music_data)


@app.get("/")
async def root():
    return music_data


@app.get("/autocomplete/db/")
async def autocomplete_v2(prefix: str, bandName: Optional[str] = None, albumTitle: Optional[str] = None) -> List[str]:
    suggestions = []
    prefix_filtered = "+".join(prefix.lower().split())
    if not bandName and not albumTitle:
        solr_results = solr_client.search(
            f"band_name:{prefix_filtered}")
        suggestions = list(set(doc["band_name"]
                           for doc in solr_results.docs if "band_name" in doc))
    elif bandName and not albumTitle:
        bandName_filtered = "+".join(bandName.lower().split())
        solr_results = solr_client.search(
            f"band_name:{bandName_filtered} AND album_title:{prefix_filtered}")
        suggestions = list(set(doc["album_title"]
                           for doc in solr_results.docs if "album_title" in doc))
    elif bandName and albumTitle:
        bandName_filtered = "+".join(bandName.lower().split())
        albumTitle_filtered = "+".join(albumTitle.lower().split())
        solr_results = solr_client.search(
            f"band_name:{bandName_filtered} AND album_title:{albumTitle_filtered } AND song_title:{prefix_filtered}")
        suggestions = list(set(doc["song_title"]
                           for doc in solr_results.docs if "song_title" in doc))
    return suggestions


@app.get("/autocomplete/trie/")
async def autocomplete_v2(prefix: str, bandName: Optional[str] = None, albumTitle: Optional[str] = None) -> List[str]:
    suggestions = []
    prefix_lower = prefix.lower()
    if not bandName and not albumTitle:
        suggestions = music_data_trie.autocomplete_bands(prefix_lower)
    elif bandName and not albumTitle:
        suggestions = music_data_trie.autocomplete_albums(
            bandName, prefix_lower)
    elif bandName and albumTitle:
        suggestions = music_data_trie.autocomplete_songs(
            bandName, albumTitle, prefix_lower)
    return suggestions


@app.get("/autocomplete/")
async def autocomplete_v1(prefix: str, bandName: Optional[str] = None, albumTitle: Optional[str] = None) -> List[str]:
    suggestions = []
    prefix_lower = prefix.lower()

    if not bandName and not albumTitle:
        suggestions = [
            band["name"]
            for band in music_data if band["name"].lower().startswith(prefix_lower)
        ]
    elif bandName and not albumTitle:
        suggestions = [
            album["title"]
            for band in music_data if band["name"].lower() == bandName.lower()
            for album in band["albums"] if album["title"].lower().startswith(prefix_lower)
        ]
    elif bandName and albumTitle:
        suggestions = [
            song["title"]
            for band in music_data if band["name"].lower() == bandName.lower()
            for album in band["albums"] if album["title"].lower() == albumTitle.lower()
            for song in album["songs"]
            if song["title"].lower().startswith(prefix_lower)
        ]

    return suggestions
