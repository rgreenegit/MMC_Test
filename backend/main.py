from typing import List, Optional
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.trie import Trie
import pysolr
import redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

solr_client = pysolr.Solr(
    'http://solr:8983/solr/autocomplete_core', timeout=10)

redis_client = redis.Redis(host='redis', port=6379,
                           db=0, decode_responses=True)

with open("data/data.json") as f:
    music_data = json.load(f)

music_data_trie = Trie()
music_data_trie.build_trie(music_data)


@app.get("/")
async def root():
    return music_data


@app.get("/autocomplete/db/")
async def autocomplete_v2(prefix: str, bandName: Optional[str] = None, albumTitle: Optional[str] = None) -> List[str]:
    try:
        suggestions = []
        prefix_filtered = "+".join(prefix.lower().split())
        cache_key = f"autocomplete:{bandName}:{albumTitle}:{prefix_filtered}"

        try:
            cached_result = redis_client.get(cache_key)
            if cached_result:
                print("Returning result from cache")
                return json.loads(cached_result)
        except redis.exceptions.RedisError as e:
            print(f"Redis error: {str(e)}")

        if not bandName and not albumTitle:
            solr_results = solr_client.search(
                f"{{!term f=band_name}}{prefix.lower()}", rows=100)
            suggestions = list(set(doc["band_name"]
                                   for doc in solr_results.docs if "band_name" in doc))

        elif bandName and not albumTitle:
            bandName_filtered = "+".join(bandName.lower().split())
            solr_results = solr_client.search(
                f"band_name:{bandName_filtered} AND {{!term f=album_title}}{prefix.lower()}", rows=100)
            suggestions = list(set(doc["album_title"]
                                   for doc in solr_results.docs if "album_title" in doc))

        elif bandName and albumTitle:
            bandName_filtered = "+".join(bandName.lower().split())
            albumTitle_filtered = "+".join(albumTitle.lower().split())
            solr_results = solr_client.search(
                f"band_name:{bandName_filtered} AND album_title:{albumTitle_filtered } AND {{!term f=song_title}}{prefix.lower()}", rows=100)
            suggestions = list(set(doc["song_title"]
                                   for doc in solr_results.docs if "song_title" in doc))

        try:
            redis_client.setex(cache_key, 10, json.dumps(suggestions))
        except redis.exceptions.RedisError as redis_error:
            print(f"Failed to cache result in Redis: {str(redis_error)}")

        return suggestions[:20]

    except pysolr.SolrError as solr_error:
        raise HTTPException(
            status_code=500, detail=f"Solr error: {str(solr_error)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching suggestions: {str(e)}")


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
