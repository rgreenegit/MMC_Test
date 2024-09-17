import requests
import json

solr_url = 'http://localhost:8983/solr/autocomplete_core/schema'
fields = ["band_name", "album_title", "song_title"]


def solr_create_field_type():
    # Create Text Field Type with NGram Tokenizer Factory & LowerCase Filter Factory
    payload = {
        "add-field-type": {
            "name": "autocomplete_text",
            "class": "solr.TextField",
            "positionIncrementGap": "100",
            "analyzer": {
                "tokenizer": {
                    "class": "solr.EdgeNGramTokenizerFactory",
                    "minGramSize": "1",
                    "maxGramSize": "20"
                },
                "filters": [
                    {"class": "solr.LowerCaseFilterFactory"}
                ]
            }
        }
    }

    headers = {
        'Content-type': 'application/json'
    }

    response = requests.post(solr_url, headers=headers,
                             data=json.dumps(payload))
    if response.status_code == 200:
        print("Field type added successfully")
    else:
        print(
            f"Error adding field type: {response.status_code}, {response.text}")


def solr_create_field():

    for field in fields:
        payload = {
            "add-field": {
                "name": field,
                "type": "autocomplete_text",
                "stored": True,
                "indexed": True
            }
        }

        headers = {
            'Content-type': 'application/json'
        }

        response = requests.post(
            solr_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Field added successfully")
        else:
            print(
                f"Error adding field: {response.status_code}, {response.text}")


if __name__ == "__main__":
    solr_create_field_type()
    solr_create_field()
