from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json


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


@app.get("/")
async def root():
    return music_data


@app.get("/autocomplete/")
async def autocomplete(prefix: str, bandName: Optional[str] = None, albumTitle: Optional[str] = None) -> List[str]:
    results = []
    prefix_lower = prefix.lower()

    if not bandName and not albumTitle:
        for band in music_data:
            band_name = band["name"]
            if band_name.lower().startswith(prefix_lower):
                results.append(band_name)

    elif bandName and not albumTitle:
        for band in music_data:
            if band["name"].lower() == bandName.lower():
                for album in band["albums"]:
                    album_title = album["title"]
                    if album_title.lower().startswith(prefix_lower):
                        results.append(album_title)

    elif bandName and albumTitle:
        for band in music_data:
            if band["name"].lower() == bandName.lower():
                for album in band["albums"]:
                    if album["title"].lower() == albumTitle.lower():
                        for song in album["songs"]:
                            song_title = song["title"]
                            if song_title.lower().startswith(prefix_lower):
                                results.append(song_title)

    return results
