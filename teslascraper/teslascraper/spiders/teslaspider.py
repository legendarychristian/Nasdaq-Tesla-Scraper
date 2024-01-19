import scrapy
import json
from teslascraper.items import StockItem


class TeslaspiderSpider(scrapy.Spider):
    name = "teslaspider"
    allowed_domains = ["www.nasdaq.com", "api.nasdaq.com"]
    start_urls = ["https://www.nasdaq.com/market-activity/quotes/real-time"]

    def parse(self, response):
        
        # getting the list of stocks from the homepage
        # this is a list of rows from the table
        stocks = response.xpath("//div[@class='manual-table__content']//table//tr")

        # storing the top stocks
        stock_item = StockItem()

        for stock in range(len(stocks)): 
            
            #getting the specific class for each row
            symbol_class = "row_"+str(stock)+" col_0"
            company_name_class = "row_"+str(stock)+" col_1"
            
            xpath_symbol_class = f"//td[@class='{symbol_class}']//a//text()"
            xpath_company_name_class = f"//td[@class='{company_name_class}']//a//text()"
    
            #storing the list in the item
            stock_item['Symbol'] = stocks[stock].xpath(xpath_symbol_class).get(),
            stock_item['Company_Name'] = stocks[stock].xpath(xpath_company_name_class).get()
            
            #getting the tesla stock url
            if stock == 2:
                xpath_next_url = f"//td[@class='{company_name_class}']//a//@href"
                next_url = stocks[stock].xpath(xpath_next_url).get()
            
            yield stock_item
            
        # going to the page of the tesla stock
        
        next_page = "https://www.nasdaq.com/" + next_url
  
        yield response.follow(next_page, meta = {'dont_redirect': True,'handle_httpstatus_list': [302]}, callback=self.get_tesla_link)
        
    def get_tesla_link(self, response):
        
        xpath_tesla_url = "//div[@class='latest-real-time-trades-link']//a//@href"
        tesla_url = response.xpath(xpath_tesla_url).get()
        next_page = "https://www.nasdaq.com/market-activity/stocks/tsla/" + tesla_url
        
        

    
        
        

        