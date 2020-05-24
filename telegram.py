#!/usr/bin/python

####
#### Usage: python telegram.py <timestamp> <telegram_bot_token> <output_dir>
####

import sys
import json
import requests

def telegram_bot_sendtext(bot_message, bot_token):
    #retrieve all chat_ids
    response = requests.get("https://api.telegram.org/bot"+bot_token+"/getUpdates")
    for d in response.json()['result']:
        bot_chatID = str(d['message']['chat']['id'])
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)

def btc_value():
    response = requests.get("https://blockchain.info/ticker")
    return str(response.json()['USD']['last'])

def getEliteScale(timestamp):
    response = requests.get("https://www.okex.com/v2/futures/pc/public/eliteScale.do?symbol=f_usd_btc&type=0&t="+str(timestamp))
    return response.json()

## ARGS and CONSTANTS
version = "0.2"
timestamp = str(sys.argv[1])
bot_token = str(sys.argv[2])
output_dir = str(sys.argv[3])
threshold = 0.50
prefix = "eliteScale-"
filename = prefix + timestamp + ".json"

data = getEliteScale(timestamp)

#backup the data
with open(output_dir + "/" + filename, 'w') as f:
    f.write(str(data))

#filter
buydata = data['data']['buydata']
selldata = data['data']['selldata']
buy_value = buydata[len(buydata) - 1]
sell_value = selldata[len(selldata) - 1]

if buy_value >= threshold or sell_value >= threshold:
    telegram_bot_sendtext("<<< WARN SENTIMENT ver. "+ version + " >>>\n" + str(buy_value) + "% LONG vs " + str(sell_value) + "% SELL \nBTC value is " + btc_value() + " $", bot_token)
