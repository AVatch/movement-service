import os
import requests

GEO_PROVIDER = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

# https://developers.google.com/places/supported_types#table1
GEO_PROVIDER_CATEGORY_EXCLUSION = [
    'locality',
    'sublocality',
    'neighborhood',
    'country',
    'postal_code',
    'administrative_area_level_1',
    'administrative_area_level_2',
    'administrative_area_level_3',
]

def process_response(response):
    """
    for now return only the first response in the search array
    as long as it is not a generic neighborhood or something
    """
    for result in response['results']:
        if not set(result['types']).intersection(set(GEO_PROVIDER_CATEGORY_EXCLUSION)):
            return {
                'name': result['name'],
                'type': result['types']         
            }
    return None


def geoSearch(lat, lng, radius=100):
    """
    perform a query against a geo provider
    """
    params = {
        'location': str(lat) + ',' + str(lng),
        'radius': radius,
        'key': os.environ.get("GEO_SERVICE_API_KEY")
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