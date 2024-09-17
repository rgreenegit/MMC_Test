from typing import List
from fastapi import FastAPI
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Data
with open("data.json") as f:
    music_data = json.load(f)


@app.get("/")
async def root():
    return music_data


@app.get("/autocomplete/")
async def autocomplete(prefix: str) -> List[str]:
    results = []
    prefix_lower = prefix.lower()

    for band in music_data:
        band_name = band["name"].lower()

        if band_name.startswith(prefix_lower):
            results.append(band_name)
    return results
