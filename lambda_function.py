
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def lambda_handler(event, context):
	
	process = CrawlerProcess(get_project_settings())

	# 'game' is the name of the spider of the project.
	process.crawl('game')
	process.start() # the script will block here until the crawling is finished

	return((event, context)