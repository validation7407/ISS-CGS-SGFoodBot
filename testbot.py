#NEED TO ADD RETURN STATEMENTS FOR RESPONSE
# NEED TO Beautify the responses

from flask import Flask, request, make_response, jsonify
import requests
from pandas.io.json import json_normalize
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="app")

app = Flask(__name__)
## TODO: STEP 1 
 # Place your API KEY Here... 
#"8a81d247d650cb16469c4ba3ceb7d265"

# **********************
# UTIL FUNCTIONS : START
# **********************
from zomathon import ZomatoAPI
API_KEY = "e6af9356ab628adc421d238f96e6fdda"
zom = ZomatoAPI(API_KEY)
#zom.cuisines
#zom.locations(query = "clementi")
# QUERY WITH LOCATION AND CUISINE

def getLocationID(location):
#    location_id = zom.locations(query=location)
#    location_id = location_id['location_suggestions'][0]['entity_id']
    location_coord = geolocator.geocode(location)
#    print(location_coord.address)
    coord = ((location_coord.latitude, location_coord.longitude))
    print(coord)
    return coord

def getjson(url):
    resp =requests.get(url)
    return resp.json()

def getCuisineInfo():
    #API_ENDPOINT = f"https://developers.zomato.com/api/v2.1/cuisines?city_id=52"
    data = zom.cuisines(city_id = 52)
    data1 = json_normalize(data['cuisines'])
    return(data1)
    
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
          
        
# **********************
# UTIL FUNCTIONS : END
# **********************

# *****************************
# Intent Handlers funcs : START
# *****************************
def find_restaurants(restaurants,n):
    final = []
#    restaurant_name =[]
#    restaurant_address = []
#    restaurant_ph = []
#    restaurant_photo =[]
#    resturant_url = []
#    restaurant_rating=[]
#    
    restaurant_details = {}
    
    for i in range(0,int(n)):
        restaurant_details[i] = {}
        restaurant_details[i]['name'] = restaurants['restaurants'][i]['restaurant']['name']
        restaurant_details[i]['address'] = restaurants['restaurants'][i]['restaurant']['location']['address']
        restaurant_details[i]['phone'] = restaurants['restaurants'][i]['restaurant']['phone_numbers']
        restaurant_details[i]['photo'] = restaurants['restaurants'][i]['restaurant']['location']['address']
        restaurant_details[i]['url'] = restaurants['restaurants'][i]['restaurant']['photos_url']
        restaurant_details[i]['rating'] = restaurants['restaurants'][i]['restaurant']['user_rating']['aggregate_rating']

#        restaurant_name.append(restaurants['restaurants'][i]['restaurant']['name'])
#        restaurant_address.append(restaurants['restaurants'][i]['restaurant']['location']['address'])
#        restaurant_ph.append(restaurants['restaurants'][i]['restaurant']['phone_numbers'])
#        restaurant_photo.append(restaurants['restaurants'][i]['restaurant']['photos_url'])
#        resturant_url.append(restaurants['restaurants'][i]['restaurant']['url'])
#        restaurant_rating.append(restaurants['restaurants'][i]['restaurant'][9]['aggregate_rating'])
#        print("Name :",restaurant_name[i])
#        print("Address : ",restaurant_address[i])
#        print("Phone Number :",restaurant_ph[i])
        final.append({
                  "title": restaurant_details[i]['name'],
                  "openUrlAction": {
                    "url": restaurant_details[i]['url']
                  },
                  "description": restaurant_details[i]['address'],
                  "footer": "Rating :"  + str(restaurant_details[i]['rating']) + "\n" + "Phone :" + restaurant_details[i]['phone'],
                  "image": {
                    "url": restaurant_details[i]['photo'],
                    "accessibilityText":restaurant_details[i]['name']
                  }
                })#,restaurant_ph[i]})
#            
#        final.append({
#                  "title": restaurant_name[i],
#                  "openUrlAction": {
#                    "url": resturant_url[i]
#                  },
#                  "description": restaurant_address[i],
#                  "footer": "Phone :" + restaurant_ph[i] + "\n" + "Rating :"  + restaurant_rating[i],
#                  "image": {
#                    "url": restaurant_photo[i],
#                    "accessibilityText": restaurant_name[i]
#                  }
#                })#,restaurant_ph[i]})
    
    #print(cuisine,location)
    
    final = final[0:4]
    final = sorted(final, key=lambda k: k['footer'],reverse=True)
    return final

def YesCuisineYesLocation(cuisine,location):
    """
    Get location parameter from dialogflow and call the util function `getWeatherInfo` to get weather info
    """
    
    info = getCuisineInfo()
    df = info[info['cuisine.cuisine_name'] == cuisine]
    cuisine_id = df.iloc[0]['cuisine.cuisine_id']
#    return f"Cuisines is \n{cuisine_name} and ID is {cuisine_id}"
    print(cuisine,cuisine_id,location)
    coord = getLocationID(location)
    restaurants = zom.search(q = location,
                             entity_type="subzone",
                             lat=coord[0],lon=coord[1],
                             cuisines = cuisine_id,
                             radius=100,
                             sort='real_distance')
    number = 10
    n = min(restaurants['results_found'],number)
    print(n)
    result = find_restaurants(restaurants,n)
    return result

def YesCuisineNoLocation(cuisine):
    
    info = getCuisineInfo()
    df = info[info['cuisine.cuisine_name'] == cuisine]
    cuisine_id = df.iloc[0]['cuisine.cuisine_id']
#    return f"Cuisines is \n{cuisine_name} and ID is {cuisine_id}"
    restaurants = zom.search(q = "Singapore",
                             entity_id=52,
                             entity_type="city",
                             cuisines = cuisine_id,
                             sort='rating')
    number = 10
    n = min(restaurants['results_found'],number)
    result = find_restaurants(restaurants,n)
    return result

def NoCuisineYesLocation(location):
#    return f"Cuisines is \n{cuisine_name} and ID is {cuisine_id}"
    restaurants = zom.search(q = location,
                             entity_type="subzone",
                             lat=coord[0],lon=coord[1],
                             radius=100,
                             sort='real_distance')
    number = 10
    n = min(restaurants['results_found'],number)
    result = find_restaurants(restaurants,n)
    return result
    
def NoCuisineNoLocation():
    restaurants = zom.search(q = "Singapore",entity_id=52,entity_type="city")
    number = 10
    n = min(restaurants['results_found'],number)
    result = find_restaurants(restaurants,n)
    return result

def SearchQuery(cuisine,location,number):
    if cuisine != "":
        info = getCuisineInfo()
        df = info[info['cuisine.cuisine_name'] == cuisine]
        cuisine_id = df.iloc[0]['cuisine.cuisine_id']
        flag1 = 1
    else:
        flag1 = 0
    if location == "":
        location = "Singapore"
        flag2 = 0
    else:
        flag2 = 1
    
    if number == "":
        number = 10
        
    print(cuisine_id,location)
    
    if flag1 == 0:
        print("Only Location found",number)
        restaurants = zom.search(q = location,
                             entity_type="subzone",
                             lat=coord[0],lon=coord[1],
                             radius=100,
                             sort='real_distance')
        n = min(restaurants['results_found'],number)
        result = find_restaurants(restaurants,n)
        return result

    elif flag1 == 1 and flag2 == 1:
        print("Location and cuisine found",number)
        restaurants = zom.search(q = location,
                             entity_type="subzone",
                             lat=coord[0],lon=coord[1],
                             cuisines = cuisine_id,
                             radius=100,
                             sort='real_distance')
        n = min(restaurants['results_found'],number)
        result = find_restaurants(restaurants,n)
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
        cuisine = req["queryResult"]["outputContexts"][1]["parameters"]["cuisines"]
        location  = req["queryResult"]["outputContexts"][1]["parameters"]["locations"]
        location = location + ", Singapore"
        print(cuisine,location)
        resp_text = YesCuisineYesLocation(cuisine,location)
        #print(resp_text)
        
    elif intent_name == "YesCuisineNoLocation":
        cuisine = req["queryResult"]["outputContexts"][1]["parameters"]["cuisines"]
        resp_text = YesCuisineNoLocation(cuisine)
        
    elif intent_name == "NoCuisineYesLocation" or intent_name == "LocationFirstAnyCuisine":
        location  = req["queryResult"]["outputContexts"][1]["parameters"]["locations"]
        location = location + ", Singapore"
        resp_text = NoCuisineYesLocation(location)
        
    elif intent_name == "NoCuisineNoLocation":
        resp_text = NoCuisineNoLocation()
        
    elif intent_name == "SearchQuery":
        cuisine = req["queryResult"]["outputContexts"][0]["parameters"]["cuisines"]
        location  = req["queryResult"]["outputContexts"][0]["parameters"]["locations"]
        location = location + ", Singapore"
        number  = req["queryResult"]["outputContexts"][0]["parameters"]["number"]
        resp_text = SearchQuery(cuisine,location,number)
#    elif intent_name == "Welcome":
#        resp_text = "Hello. I'm SGFoodBot. What would you like to have today ? You can start by typing a Cuisine, a location or a query."
    else:
        resp_text = "Unable to find a matching intent. Try again."
    #print(resp_text)
    return make_response(jsonify({
            "fulfillmentText": "Alright, here's a list of restaurants for you",
  "fulfillmentMessages": getCardList(resp_text,5),
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
            "title": "Make another query"
          },
          {
            "title": "End Convo"
          }
        ],
    "linkOutSuggestion": {
          "destinationName": "Another Query",
          "url": "https://assistant.google.com/services/invoke/uid/00000079f9fd6f18?hl=en"
      }
    }
    }
    }
  }
))

# ***************************
# WEBHOOK MAIN ENDPOINT : END
# ***************************

if __name__ == '__main__':
    app.run(debug=False)
