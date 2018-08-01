import scrapy
import sys
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import json
import requests
import googlemaps
import configparser

#Ensure that a .ini file named keys.ini is present in the scrapy project directory and
# it contains all the needed values below.  
config = configparser.ConfigParser()
config.read('keys.ini')
MAILGUN_API_KEY = config['keys']['mailgun_api_key']
ITAD_API_KEY = config['keys']['itad_api_key']
GOOGLE_MAPS_API_KEY = config['keys']['google_maps_api_key']
OATH_CLIENT_ID = config['keys']['oath_client_id']
OATH_CLIENT_SECRET = config['keys']['oath_client_secret']
gmaps = googlemaps.Client(key=str(GOOGLE_MAPS_API_KEY))
CLIENT_NAME = config['keys']['client_name']
CLIENT_EMAIL = config['keys']['client_email'] 
MAILGUN_DOMAIN = config['keys']['mailgun_domain'] 


#TODO: Look into unit testing (start here: https://stackoverflow.com/questions/6456304/scrapy-unit-testing)

#TO USE: scrapy crawl game_spider -a category=deals

#TODO: Use scrapy arguments to choose task that spider will perform / create different spider

ITAD_REGIONS = json.loads(requests.get('https://api.isthereanydeal.com/v01/web/regions/').text)

#print(json.dumps(ITAD_REGIONS, indent=4, sort_keys=True))
REGIONS = {}

for each in ITAD_REGIONS['data']:
    REGIONS[each] = ITAD_REGIONS['data'][each]    

#TODO: Unit test to see if reverse geocode request will have the country code in the same JSON object in the JSON list response 

GEO_LOCATION_REQUEST = json.loads(requests.post("https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBJVwNotqwF5FFwoJeoD7eaVNb8LUDY1XU").text)
GEO_LOCATION = GEO_LOCATION_REQUEST['location']
LATITUDE = GEO_LOCATION['lat'] 
LONGITUDE = GEO_LOCATION['lng']

#Rerverse geocoding request
REVERSE_GEOCODING_REQUEST = gmaps.reverse_geocode((LATITUDE, LONGITUDE))
PARSED_REVERSE = json.dumps(REVERSE_GEOCODING_REQUEST[0], indent=4, sort_keys=True)


#print(PARSED_REVERSE)

for each in REVERSE_GEOCODING_REQUEST[0]['address_components']:
        if "country" in each['types']:
                COUNTRY = each['short_name']
                break

print(COUNTRY)

QUERY_REGION = ''

for each in REGIONS:
    
    if COUNTRY in REGIONS[each]['countries']:
        #print(REGIONS[each]['countries'])
        QUERY_REGION = str(each)

#print(QUERY_REGION)

 
class GameDealSpider(scrapy.Spider):
    name = 'game_spider'
    #start_urls = ['https://isthereanydeal.com/']

    def __init__(self, category=None, *args, **kwargs):
        super(GameDealSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://api.isthereanydeal.com/v01/%s/list/?key=%s&region=%s&=country=%s' % (category.lower(), ITAD_API_KEY, QUERY_REGION, COUNTRY)]
        
    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_httpbin,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)
        
    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        jsonresponse = json.loads(response.body_as_unicode())
        pretty_json_response = json.dumps(jsonresponse, indent=4, sort_keys=True)
        #print("RESPONSE" + str(pretty_json_response))
        currency = jsonresponse['.meta']['currency']
        formatted_games = []
        for game in jsonresponse['data']['list']:


            game_str = ("\n*-----------------------*\n"
                  + game['title'] + "\n"
                  + "-------------------------\n"
                  "{0:.2f}".format(game['price_new']) + " " + currency + "\n"
                  "{0:.2f}".format(game['price_old']) + " " + currency + "\n"
                  + str(game['price_cut'])  + "%" + " off" + "\n" 
                  + "Buy this game at: " + str(game['urls']['buy']) + "\n"
                  + "*-----------------------*\n"
            )
            #print(game_str)
            formatted_games.append(game_str)

        send_simple_message(formatted_games)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

#TODO: Send email with formatted game deals 
#TODO: Consider using AWS Lambda, Azure functions (serverless computing) or just do an instance on DigitalOcean 

def send_simple_message(formatted_games):

    text = ""
    for each in formatted_games:
        text += each
    return requests.post(
        "https://api.mailgun.net/v3/sandbox93efa5bb89944484abb661b5a4349b2d.mailgun.org/messages",
        auth=("api", "" + str(MAILGUN_API_KEY)),
        data={"from": "Mailgun Sandbox " + str(MAILGUN_DOMAIN),
              "to": str(CLIENT_NAME) + " " + str(CLIENT_EMAIL),
              "subject": "Latest deals from isthereanydeal.com",
              "text": "Hi! Here are the latest deals from isthereanydeal.com!\n\n" + text})