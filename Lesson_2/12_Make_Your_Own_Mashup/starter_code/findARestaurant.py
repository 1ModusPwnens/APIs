import json
import requests
import httplib2

import sys
import codecs
from credentials import FOURSQUARE_CLIENT_ID, FOURSQUARE_CLIENT_SECRET, GOOGLE_API_KEY
#sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = FOURSQUARE_CLIENT_ID
foursquare_client_secret = FOURSQUARE_CLIENT_SECRET
google_api_key = GOOGLE_API_KEY
h = httplib2.Http()

def getGeocodeLocation(inputString):
    # Use Google Maps to convert a location into Latitute/Longitute coordinates
    # FORMAT: https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=API_KEY
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    result = json.loads(h.request(url,'GET')[1])
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude,longitude)

def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	coords = getGeocodeLocation(location)

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	request_params = dict(client_id=foursquare_client_id, client_secret=foursquare_client_secret, v=20180323, ll='{0},{1}'.format(coords[0],coords[1]), query=mealType, limit=1, intent='browse')
	response = requests.get(url='https://api.foursquare.com/v2/venues/explore', params=request_params)
	result = json.loads(response.text)

	#3. Grab the first restaurant
	venue_name = result['response']['groups'][0]['items'][0]['venue']['name']
	venue_id = result['response']['groups'][0]['items'][0]['venue']['id']
	venue_address = ', '.join(result['response']['groups'][0]['items'][0]['venue']['location']['formattedAddress'])

	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	img_response = requests.get(url='https://api.foursquare.com/v2/venues/%s/photos' % venue_id, params=dict(client_id=foursquare_client_id, client_secret=foursquare_client_secret, v=20180323, limit=1))
	
	#5. Grab the first image
	try:
		img_url = img_response.json()['response']['photos']['items'][0]['prefix'] + '300x300' + img_response.json()['response']['photos']['items'][0]['suffix']
	#6. If no image is available, insert default a image url
	except IndexError:
		img_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/socialmedia/apple/198/pile-of-poo_1f4a9.png"

	#7. Return a dictionary containing the restaurant name, address, and image url	
	return {
	'Restaurant Name: ': venue_name,
	'Restaurant Address: ': venue_address,
	'Image: ': img_url
	}

if __name__ == '__main__':

	print(findARestaurant("Pizza", "Tokyo, Japan"))
	print(findARestaurant("Tacos", "Jakarta, Indonesia"))
	print(findARestaurant("Tapas", "Maputo, Mozambique"))
	print(findARestaurant("Falafel", "Cairo, Egypt"))
	print(findARestaurant("Spaghetti", "New Delhi, India"))
	print(findARestaurant("Cappuccino", "Geneva, Switzerland"))
	print(findARestaurant("Sushi", "Los Angeles, California"))
	print(findARestaurant("Steak", "La Paz, Bolivia"))
	print(findARestaurant("Gyros", "Sydney, Australia"))
