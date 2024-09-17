import json
import pysolr
import argparse

solr_client = pysolr.Solr(
    'http://localhost:8983/solr/autocomplete_core', timeout=10)

with open("../data.json", 'r') as file:
    data = json.load(file)

names = []
album_titles = []
song_titles = []

parsed_data = []

for artist in data:
    for album in artist.get("albums", []):
        for song in album.get("songs", []):
            parsed_data.append(
                {"band_name": artist.get("name"), "album_title": album.get("title"), "song_title": song.get("title")})

print(parsed_data[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process data for Solr.")
    parser.add_argument('--upload', action='store_true',
                        help='Upload data to Solr')
    args = parser.parse_args()

    if args.upload:
        # Upload data to Solr
        solr_client.add(parsed_data)
        solr_client.commit()

    results = solr_client.search('{!term f=band_name}ram')
    for result in results:
        print(result)
