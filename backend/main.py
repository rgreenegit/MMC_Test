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
    suggestions = []
    prefix_lower = prefix.lower()

    if not bandName and not albumTitle:
        suggestions = [
            band["name"] for band in music_data if band["name"].lower().startswith(prefix.lower())]

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
