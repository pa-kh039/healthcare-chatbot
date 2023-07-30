import requests
from conf import RapidAPI_Key,google_apikey

def find_nearby_docs(pincode=440030):
    try:
        pincode=int(pincode) #converting from string to integer
    except:
        return "Invalid pincode. Give valid indian pin code in valid format (as mentioned)."
    
    url = "https://india-pincode-with-latitude-and-longitude.p.rapidapi.com/api/v1/pincode/{}".format(pincode) #fetching probable coordinates from pincode
    headers = {
        "X-RapidAPI-Key": RapidAPI_Key,
        "X-RapidAPI-Host": "india-pincode-with-latitude-and-longitude.p.rapidapi.com"
    }
    response = (requests.get(url, headers=headers)).json()
    latitude=response[0]['lat']
    longitude=response[0]['lng']
    radius=1000

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}%2C{}&radius={}&type=hospital&key={}".format(latitude,longitude,radius,google_apikey)  #fetching nearby hospitals using google places API
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    ans="Here are some hospitals close to your location:"
    for place in (response.json())['results']:   #adding hospitals from response one-by-one to the text to be returned
        txt="\n Name:{},\n Rating:{}, Address:{};".format(place['name'],place['rating'] if 'rating' in place.keys() else "NA",place['vicinity'])
        ans+=txt
    return ans
