'''
get_yelp_data.py
author: Steven Jackowski
created date: April 21, 2018
'''

import json
import requests

# API Config parameters
API_URL = "https://api.yelp.com/v3/businesses/search"
API_CONFIG_FILE = "api_config.json"

# Search constants - used to loop through the following cities and search categories
LOCATIONS = ["Denver, CO", "Portland, OR", "Sacramento, CA"]
#CATEGORIES = ["coffee", "breweries", "bikes"]
CATEGORIES = ["bikes"]

def get_api_key(api_config_file):
    '''
    Takes the name of a config file and returns the api key.
    The filename should point to a JSON file with a key-value pair called
    'api_key'.
    '''
    with open(api_config_file) as api:
        conf = json.load(api)
    return conf["api_key"]


def get_request(location, category, api_key, api_url, offset):
    '''
    Sends the request to the yelp API with the provided parameters.
    '''
    auth_header = {"Authorization": "Bearer %s" %api_key}
    params = {"location": location,
              "categories": category,
              "limit": 50,
              "offset": offset}
    r = requests.get(api_url, headers=auth_header, params=params)
    r.raise_for_status()
    return r
    # if r.status_code == "200":
    #     return r
    # else:
    #     raise HTTPError(r.url, r.status_code, r.text, r.headers, r)


if __name__ == "__main__":
    API_KEY = get_api_key(API_CONFIG_FILE)

    for location in LOCATIONS:
        for category in CATEGORIES:
            out_fname = u'data/' + location.split(',')[0] + '_' + category + '.json'

            offset_count = 0

            # Initial request
            r = get_request(location, category, API_KEY, API_URL, offset_count)
            r_json = r.json()
            businesses = r_json["businesses"]
            total = r_json["total"]
            offset_count += 50

            # API only returns 50 results at a time, so we need to keep sending requests until there
            # are no more results
            while offset_count < total:
                r = get_request(location, category, API_KEY, API_URL, offset_count)
                r_json = r.json()
                businesses.extend(r_json["businesses"])
                offset_count += 50

            with open(out_fname, 'w') as out_json:
                json.dump(businesses, out_json)
    