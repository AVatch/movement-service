import os
import requests

GEO_PROVIDER = 'https://api.foursquare.com/v2/venues/search'

# https://developers.google.com/places/supported_types#table1
GEO_PROVIDER_CATEGORY_EXCLUSION = [
    "530e33ccbcbc57f1066bbfe4",
    "50aa9e094b90af0d42d5de0d",
    "5345731ebcbc57f1066c39b2",
    "530e33ccbcbc57f1066bbff7",
    "4f2a25ac4b909258e854f55f",
    "530e33ccbcbc57f1066bbff8",
    "530e33ccbcbc57f1066bbff3",
    "530e33ccbcbc57f1066bbff9"
]

def process_response(response):
    """
    for now return only the first response in the search array
    as long as it is not a generic neighborhood or something
    """
    for result in response['response']['venues']:
        if not set(result['categories'][0]['id']).intersection(set(GEO_PROVIDER_CATEGORY_EXCLUSION)):
            return {
                'name': result['name'],
                'type': result['categories'][0]['pluralName']
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
