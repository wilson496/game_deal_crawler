#TODO: Migrate this project to AWS Lambda and use this to run it

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def lambda_handler(event, context):
	process = CrawlerProcess(get_project_settings())
	process.crawl('game')
	process.start()
	return((event)
