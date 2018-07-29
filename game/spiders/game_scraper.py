import scrapy
import sys
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import json
import requests
import googlemaps

#TODO: FIX THESE UPON RELEASE 
ITAD_API_KEY = "9499128e51c390fc4c015db0185a824f0abb3cd4"
gmaps = googlemaps.Client(key="AIzaSyBJVwNotqwF5FFwoJeoD7eaVNb8LUDY1XU")
OATH_CLIENT_ID = "08be3a658c5a5e8c"
OATH_CLIENT_SECRET = "6d954cf6cac888371b0a5af137b9d7d96366ef3a"



#TODO: Look into unit testing (start here: https://stackoverflow.com/questions/6456304/scrapy-unit-testing)

#TO USE: scrapy crawl game_spider -a category=deals

#TODO: Use scrapy arguments to choose task that spider will perform / create different spider

ITAD_REGIONS = json.loads(requests.get('https://private-ddbf55-itad.apiary-mock.com/v01/web/regions/').text)
print(json.dumps(ITAD_REGIONS, indent=4, sort_keys=True))
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

COUNTRY = REVERSE_GEOCODING_REQUEST[0]['address_components'][6]['short_name']
#print(COUNTRY)

QUERY_REGION = ''

for each in REGIONS:
    
    if COUNTRY in REGIONS[each]['countries']:
        print(REGIONS[each]['countries'])
        QUERY_REGION = str(each)

print(QUERY_REGION)

 
class GameDealSpider(scrapy.Spider):
    name = 'game_spider'
    #start_urls = ['https://isthereanydeal.com/']

    def __init__(self, category=None, *args, **kwargs):
        super(GameDealSpider, self).__init__(*args, **kwargs)
        
        #URLS to parse
        #self.start_urls = ['https://private-ddbf55-itad.apiary-mock.com/v01/%s/list/?%s&region=%s' % (category.lower(), ITAD_API_KEY, QUERY_REGION)]
        
        #TODO: Use if/when granted access to production 
        self.start_urls = ['https://api.isthereanydeal.com/v01/%s/list/?%s&region=%s' % (category.lower(), ITAD_API_KEY, QUERY_REGION)]
        

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_httpbin,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)
        
    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        print("RESPONSE" + str(response.body))
        # do something useful here...

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