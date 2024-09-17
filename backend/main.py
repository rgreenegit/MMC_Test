from typing import List, Optional
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from trie import Trie

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    prefix_lower = prefix.lower()
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
