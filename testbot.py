from flask import Flask, request, make_response, jsonify
import requests
from pandas.io.json import json_normalize
from zomathon import ZomatoAPI
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="app")

app = Flask(__name__)
API_KEY = "f91c97ff34995539b40868a1e3ae5c84"
zom = ZomatoAPI(API_KEY)

# **********************

# UTIL FUNCTIONS : START

# **********************

def getjson(url):
    resp =requests.get(url)
    return resp.json()

def getCuisineInfo():
    #API_ENDPOINT = f"https://developers.zomato.com/api/v2.1/cuisines?city_id=52"
    data = zom.cuisines(city_id = 52)
    data1 = json_normalize(data['cuisines'])

    return data1

def getEntityId(locationz):
     data = zom.locations(query=locationz)
     return data


def latlong(location):
    loc = geolocator.geocode(location)
    return (loc.latitude, loc.longitude)


def getCardList(resp_text,n):
    temp =[]
    try:
        for i in range(n):
            card = {
              "card":{
                "title": resp_text[i]['title'],
                "subtitle": resp_text[i]['description'],
                "buttons": [
                  {
                    "text": resp_text[i]['title'],
                    "postback": resp_text[i]["openUrlAction"]["url"]
                    }]
                  }}
            temp.append(card)
    except:
        temp = "Sorry I could not find any restaurants here, would you like to make another request?"
    return temp

def find_restaurants(restaurants, n):

     final = []
     restaurant_name = []
     restaurant_address = []
     restaurant_ph = []
     restaurant_photo = []
     resturant_url = []
     restaurant_rating = []
     
     for i in range(0, int(n)):

          restaurant_name.append(restaurants['restaurants'][i]['restaurant']['name'])
          restaurant_address.append(restaurants['restaurants'][i]['restaurant']['location']['address'])
          restaurant_ph.append(restaurants['restaurants'][i]['restaurant']['phone_numbers'])
          restaurant_photo.append(restaurants['restaurants'][i]['restaurant']['photos_url'])
          resturant_url.append(restaurants['restaurants'][i]['restaurant']['url'])
          restaurant_rating.append(restaurants['restaurants'][i]['restaurant']['user_rating']['aggregate_rating'])
          #        print("Name :",restaurant_name[i])
          #        print("Address : ",restaurant_address[i])
          #        print("Phone Number :",restaurant_ph[i])
          final.append({

               "title": restaurant_name[i],

               "openUrlAction": {

                    "url": resturant_url[i]

               },

               "description": restaurant_address[i],

               "footer": "Phone :" + restaurant_ph[i],#"Rating : " + str(restaurant_rating[i]) + "\nPhone :" + restaurant_ph[i] ,

               "image": {

                    "url": restaurant_photo[i],

                    "accessibilityText": restaurant_name[i]

               }

          })  # ,restaurant_ph[i]})


    
     #final = sorted(final, key = lambda i: i['footer'], reverse = True)
     #print(final)
     return final
     

# **********************

# UTIL FUNCTIONS : END

# **********************

# *****************************

# Intent Handlers funcs : START

# *****************************

def YesCuisineYesLocation(cuisine,location):
    info = getCuisineInfo()
    df = info[info['cuisine.cuisine_name'] == cuisine]
    cuisine_id = df.iloc[0]['cuisine.cuisine_id']
#    outp = getEntityId(location)#
#    location_id = outp['location_suggestions'][0]['entity_id']
    loc = latlong(location)
    lat = loc[0]
    long = loc[1]
    print(lat,long)
    # print(cuisine, cuisine_id, location, location_id)
#    restaurants = zom.search(entity_id=location_id, entity_type='subzone', cuisines=int(cuisine_id), sort='rating', order='desc')
    restaurants = zom.search(q = location, cuisines=int(cuisine_id), lat = lat, lon = long, sort = 'real_distance', radius = 3000)
    number = 10
    n = min(restaurants['results_found'], number)
    result = find_restaurants(restaurants, n)
    return result

def YesCuisineNoLocation(cuisine):
    info = getCuisineInfo()
    df = info[info['cuisine.cuisine_name'] == cuisine]
    cuisine_id = df.iloc[0]['cuisine.cuisine_id']
    # print(cuisine, cuisine_id)
    restaurants = zom.search(entity_id=52, entity_type='city', cuisines=int(cuisine_id),sort = 'rating', order = 'desc')
    number = 10
    n = min(restaurants['results_found'],number)
    result = find_restaurants(restaurants, n)
    return result

def NoCuisineYesLocation(location):
     #outp = getEntityId(location)
     loc = latlong(location)
     lat = loc[0]
     long = loc[1]
     print(lat,long)
    # print(cuisine, cuisine_id, location, location_id)
#    restaurants = zom.search(entity_id=location_id, entity_type='subzone', cuisines=int(cuisine_id), sort='rating', order='desc')
     restaurants = zom.search(q = location,  lat = lat, lon = long, sort = 'real_distance', radius = 3000)
     number = 10
     n = min(restaurants['results_found'], number)
     result = find_restaurants(restaurants, n)
     return result

def NoCuisineNoLocation():
     restaurants = zom.search(entity_id=52, entity_type='city', sort='rating', order='desc')
     number = 10
     n = min(restaurants['results_found'], number)
     result = find_restaurants(restaurants, n)
     return result

def SearchQuery(cuisine,location,number):

    if cuisine != "":
          info = getCuisineInfo()
          df = info[info['cuisine.cuisine_name'] == cuisine]
          cuisine_id = df.iloc[0]['cuisine.cuisine_id']
          c_flag = 1
    else:
          c_flag = 0

    if location == "":
          location = "Singapore"
          location_id = 52
          l_flag = 0

    else:
         #location += ", Singapore"
         outp = getEntityId(location)
         #location_id = outp['location_suggestions'][0]['entity_id']
         loc = latlong(location)
         lat = loc[0]
         long = loc[1]
         l_flag = 1

    if number == "":
        number = 10
    print(cuisine_id,location)

    if c_flag == 0:

        print("Only Location found",number)
        restaurants = zom.search(q = location,  lat = lat, lon = long, sort = 'real_distance', radius = 3000)
        n = min(restaurants['results_found'], int(number))
        result = find_restaurants(restaurants, n)
        return result

    elif c_flag == 1 and l_flag == 1:

        print("Location and cuisine found",number)
        info = getCuisineInfo()
        df = info[info['cuisine.cuisine_name'] == cuisine]
        cuisine_id = df.iloc[0]['cuisine.cuisine_id']

        # print(cuisine, cuisine_id, location, location_id)

        restaurants = zom.search(q = location, cuisines=int(cuisine_id), lat = lat, lon = long, sort = 'real_distance', radius = 2000)
        n = min(restaurants['results_found'], int(number))
        result = find_restaurants(restaurants, n)
        return result

# ***************************

# Intent Handlers funcs : END

# ***************************

# *****************************

# WEBHOOK MAIN ENDPOINT : START

# *****************************

@app.route('/', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]
    print("INTENT FIRED : ", intent_name)

    if intent_name == "YesCuisineYesLocation" or intent_name == "LocationFirstCuisine":
        cuisine = req["queryResult"]["outputContexts"][-1]["parameters"]["cuisines"] # CHANGE LIST INDEX FOR DIFFERENT BOTS
        location  = req["queryResult"]["outputContexts"][-1]["parameters"]["locations"]
        location += ", Singapore"
        print(cuisine, location)
        resp_text = YesCuisineYesLocation(cuisine,location)

    elif intent_name == "YesCuisineNoLocation":
        cuisine = req["queryResult"]["outputContexts"][-1]["parameters"]["cuisines"]
        resp_text = YesCuisineNoLocation(cuisine)

    elif intent_name == "NoCuisineYesLocation" or intent_name == "LocationFirstAnyCuisine":
        location  = req["queryResult"]["outputContexts"][-1]["parameters"]["locations"]
        location += ", Singapore"
        resp_text = NoCuisineYesLocation(location)

    elif intent_name == "NoCuisineNoLocation":
        resp_text = NoCuisineNoLocation()
        
    elif intent_name == "SearchQuery":
        cuisine = req["queryResult"]["outputContexts"][0]["parameters"]["cuisines"]
        location  = req["queryResult"]["outputContexts"][0]["parameters"]["locations"]
        location += ", Singapore"
        number  = req["queryResult"]["outputContexts"][0]["parameters"]["number"]
        resp_text = SearchQuery(cuisine,location,number)
    else:
        resp_text = "Unable to find a matching intent. Try again."
    
    print(resp_text)
    
    l = len(resp_text)

    if len(resp_text) != 0:
        return make_response(jsonify({
        "fulfillmentText": "Alright, here's a list of restaurants for you",
        "fulfillmentMessages": getCardList(resp_text,l),
      "payload": {
        "google": {
          "expectUserResponse": True,
          "richResponse": {
            "items": [
              {
                "simpleResponse": {
                  "textToSpeech": "Here is a list of Restaurants.",
                  "displayText" : "Here is a list of Restaurants."
                }
              },
              {
                "carouselBrowse": {
                  "items": resp_text,
                }
              }
            ],
        "suggestions": [
              {
                "title": "Another Query"
              },
              {
                "title": "End Convo"
              }
            ]
        }
        }
      }
    }))
    else:
        return make_response(jsonify(
                {
    "fulfillmentText": "Oops. Seems like there are no restaurants for that search. Sorry!",
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "Oops. Seems like there are no restaurants for that search. Sorry!",
              "displayText": "Oops. Seems like there are no restaurants for that search. Sorry!"
            }
          }
        ],
    "suggestions": [
              {
                "title": "Another Query"
              },
              {
                "title": "End Convo"
              }
            ]
      }
    }
  }
}))

# ****************************

# WEBHOOK MAIN ENDPOINT : END

# ***************************
if __name__ == '__main__':
   app.run(debug=False)
