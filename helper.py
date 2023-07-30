import requests
from conf import RapidAPI_Key,google_apikey

def find_nearby_docs(pincode=440030):
    try:
        pincode=int(pincode)
    except:
        return "Invalid pincode. Give valid indian pin code in valid format (as mentioned)."
    
    #fetching probable coordinates from pincode
    url = "https://india-pincode-with-latitude-and-longitude.p.rapidapi.com/api/v1/pincode/{}".format(pincode)

    headers = {
        "X-RapidAPI-Key": RapidAPI_Key,
        "X-RapidAPI-Host": "india-pincode-with-latitude-and-longitude.p.rapidapi.com"
    }

    response = (requests.get(url, headers=headers)).json()
    latitude=response[0]['lat']
    # latitude=19.0760
    longitude=response[0]['lng']
    # longitude=72.8777

    # fetching nearby health-centres from coordinates
    # url = 'https://nominatim.openstreetmap.org/search'
    # params = {
    #     'format': 'json',
    #     'lat': latitude,
    #     'lon': longitude,
    #     'radius': 10000,
    #     'q': "hospital",
    #     'country_codes': 'IN'
    # }

    # response = requests.get(url, params=params)
    # if response.status_code == 200:
    #     data = response.json()
    #     ans="Here are some hospitals close to your location:"
    #     for place in data:
    #         txt="\n {}".format(place['display_name'])
    #         ans+=txt
    #     return ans
    # else:
    #     print(f"Error: Unable to fetch data. Status code: {response.status_code}")
    #     return None
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}%2C{}&radius=1000&type=hospital&key={}".format(latitude,longitude,google_apikey)
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    ans="Here are some hospitals close to your location:"
    for place in (response.json())['results']:
        # print(place)
        # break
        txt="\n Name:{},\n Rating:{}, Address:{};".format(place['name'],place['rating'] if 'rating' in place.keys() else "NA",place['vicinity'])
        ans+=txt
    # print(ans)
    return ans
    # print(len(response.text))
    # print(response.text)
# find_nearby_docs()