# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule #import crawl spider and rule to stablish boundaries and recursion behavior
from scrapy.linkextractors import LinkExtractor 
from deathpoetry.items import DeathpoetryItem
from bs4 import BeautifulSoup

#from bs4 import BeautifulSoup
#import urllib.request
constanturl= 'http://poetrycircle.com/forum/'
class DeathtextSpider(CrawlSpider):	
    name = 'deathtext'
    
    allowed_domains = ('poetrycircle.com',)
    start_urls = ['https://poetrycircle.com/forum/forums/submit-your-poetry.3/']
    
    rules=( 
    	Rule(LinkExtractor(allow=(), restrict_css=('.items',)), callback ="parse_item",follow=True),)
    def parse_item(self, response):
    	
        item_links=response.css('.title > a::attr(href)').extract()
        for a in item_links:
        	
        	linky = constanturl + a
        	yield scrapy.Request(linky,callback=self.parse_detail_page)
        	

    def parse_detail_page(self,response):

    	#print('URL:'+ response.url )  
    	#self.counter+=1
    	item=DeathpoetryItem()
    	poem=''.join(response.css('ol>li:nth-child(1) > .messageInfo.primaryContent >.messageContent > article').extract())
    	soup=BeautifulSoup(poem,'lxml')
    	print(soup.text)
    	item['text']=soup.text
    	yield item
