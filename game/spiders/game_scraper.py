import scrapy
import sys

#TODO: FIX THESE UPON RELEASE 
API_KEY = "d861afa6ecc8f07db0c26ae88c82c486"
OATH_CLIENT_ID = "08be3a658c5a5e8c"
OATH_CLIENT_SECRET = "6d954cf6cac888371b0a5af137b9d7d96366ef3a"


#TO USE: scrapy crawl game_spider -a category=deals

#TODO: Use scrapy arguments to choose task that spider will perform / create different spider

#https://api.isthereanydeal.com/v01/deals/list/?key=d861afa6ecc8f07db0c26ae88c82c486


class GameDealSpider(scrapy.Spider):
    name = 'game_spider'
    #start_urls = ['https://isthereanydeal.com/']

    def __init__(self, category=None, *args, **kwargs):
        super(GameDealSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://api.isthereanydeal.com/v01/%s/list/?%s' % (category.lower(), API_KEY)]
    '''
    def parse(self, response):
        SET_SELECTOR = '.game'
        for game in response.css(SET_SELECTOR):
            
            NAME_SELECTOR = 'div div ::text'
            #'name': game.css(NAME_SELECTOR).extract(),
            yield {
                'name': game.css(NAME_SELECTOR).extract(),#_first(),    
            }
    '''        