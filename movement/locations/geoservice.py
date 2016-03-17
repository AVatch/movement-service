import os
import requests

GEO_PROVIDER = 'https://api.foursquare.com/v2/venues/search'

# https://developers.google.com/places/supported_types#table1
GEO_PROVIDER_CATEGORY_EXCLUSION = [
    
]

def process_response(response):
    """
    for now return only the first response in the search array
    as long as it is not a generic neighborhood or something
    """
    for result in response['response']['venues']:
        if not set(result['categories'][0]['name']).intersection(set(GEO_PROVIDER_CATEGORY_EXCLUSION)):
            return {
                'name': result['name'],
                'type': result['categories'][0]['name']         
            }
    return None


def geoSearch(lat, lng, radius=100):
    """
    perform a query against a geo provider
    """
    params = {
        'll': str(lat) + ',' + str(lng),
        'client_id': os.environ.get("FOURSQUARE_CLIENT_ID"),
        'client_secret': os.environ.get("FOURSQUARE_CLIENT_SECRET"),
        'v': os.environ.get("FOURSQUARE_V")
    }
    response = requests.get(GEO_PROVIDER, params=params)
    if response.status_code == 200:
        return process_response( response.json() )
    else:
        return None
    
if __name__=='__main__':
    # from os.path import join, dirname
    # from dotenv import load_dotenv
    # dotenv_path = join(dirname(__file__), '../movement/.env')
    # load_dotenv(dotenv_path)
    
    # print geoSearch(-33.8670,151.1957)
    pass
