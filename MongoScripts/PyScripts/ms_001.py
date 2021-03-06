
import urllib.request
from datetime import datetime
from pprint import pprint
from pymongo import MongoClient
from alpha_vantage.timeseries import TimeSeries


####################################################################

# simple variables
now = str(datetime.today())
info_source = 'Alpha Vantage'

# Connection to the MongoDB program at specific URLs & Ports
# default is localhost:27017
connection = MongoClient('localhost:27017')

# Switching to a specific Database within MongoDB
db = connection.StockMarketDB

# Switching to a specific Collection(table) within the DB
col = db.monthlyStatistics


####################################################################

# Personal issued key from alpha_vantage
ts = TimeSeries(key='II0VU3FTX7AAEU99')

# Calling an individual company's monthly stock data
data, meta_data  = ts.get_monthly(symbol='MSFT')

scope = monthly

# Will display that data
# pprint(meta_data)

parsed_data = {}

# formatting nested dictionary keys for mongoDB
for date, stock in data.items():
    parsed_data[date] = {}
    for price in stock.keys():
        parsed_data[date][price[3:]] = data[date][price] 


#adding 'date' dictionary key as a value to
# nested dictionary, then inserting to MongoDB
for date, stock in parsed_data.items():
    stock['ticker'] = meta_data['2. Symbol']
    stock['info_source'] = info_source
    stock['last_updated'] = now
    stock['date'] = date
    stock['scope'] = scope
    col.insert_one(stock)

########################################
#            Data break down           #
########################################
# data/parsed_data                     #
# |                                    #
# -----------                          #
# |         |                          #
# date      stock                      #
#               |                      #
# ---------------------------------    #
# |     |      |     |    |       |    #
# open  close  high  low  volume  date #
########################################


###################################################################
# Looking at documents inside the collection
# for doc in col.find().sort('date', pymongo.ASCENDING):
#     pprint(doc)


# to delete all date in the collection
# mo.delete_many({})


