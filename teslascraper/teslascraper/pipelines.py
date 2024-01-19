# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TeslascraperPipeline:
    def process_item(self, item, spider):
        return item

import mysql.connector

class SaveStockListToMySqlPipeline:
    
    def __init__(self):
        self.conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'password', 
        database = 'stock_list'
        )
        
        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS stocks(
            Symbol text,
            Company_Name text
        )
        """)
        
    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into stocks(
            Symbol, 
            Company_name
            ) values (
                %s,
                %s
                )""", (
            # I got an error message here that said:
            # "python tuble cannot be converted to mysql type"
            # check for random tuples i guess
            str(item["Symbol"][0]),
            "".join(map(str, item["Company_Name"]))
        ))

        # ## Execute insert of data into database
        self.conn.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
