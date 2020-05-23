#!/usr/bin/python

####
#### Usage: python telegram.py <okex-eliteScale.json> <telegram_bot_token>
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

filename = str(sys.argv[1])
bot_token = str(sys.argv[2])
threshold = 0.50

with open(filename) as f:
  data = json.load(f)

#filter
buydata = data['data']['buydata']
selldata = data['data']['selldata']
buy_value = buydata[len(buydata) - 1]
sell_value = selldata[len(selldata) - 1]

if buy_value >= threshold or sell_value >= threshold:
    telegram_bot_sendtext("<<<WARN SENTIMENT >>>\n" + str(buy_value) + "% LONG vs " + str(sell_value) + "% SELL \nBTC value is " + btc_value() + " $", bot_token)
