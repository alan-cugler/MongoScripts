# Python2.7 Script for Ubuntu 16.04
# scp -P 2222 <FILE> vagrant@127.0.0.1:/home/vagrant/<FILE>

import os
from pprint import pprint
from pymongo import MongoClient
from alpha_vantage.timeseries import TimeSeries
    
####################################################################


# Connection to the MongoDB program at specific URLs & Ports
# default is localhost:27017
connection = MongoClient('localhost:27017')

# Switching to a specific Database within MongoDB
db = connection.StockMarketDB

# Switching to a specific Collection(table) within the DB
mo = db.monthlyStatistics

####################################################################


# Personal issued key from alpha_vantage
ts = TimeSeries(key='II0VU3FTX7AAEU99')

# Calling an individual company's monthly stock data
data, meta_data  = ts.get_monthly(symbol='MSFT')

# Will display that data
#pprint(data)

parsed_data = {}

# formatting nested dictionary keys for mongoDB
for date, stock in data.iteritems():
    parsed_data[date] = {}
    for price in stock.iterkeys():
        parsed_data[date][price[3:]] = data[date][price]

# adding 'date' dictionary key as a value to
# nested dictionary, then inserting to MongoDB
for date, stock in parsed_data.iteritems():
    stock['date'] = date
    mo.insert_one(stock)

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
# results = mo.find()
# for documents in results:
#     pprint(documents)


# to delete all date in the collection
# mo.delete_many({})
