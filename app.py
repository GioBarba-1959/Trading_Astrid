import json, os
from xml.etree.ElementTree import tostring
import ccxt
from time import sleep
from datetime import datetime
from binance.client import Client
from binance.enums import *

from flask import Flask, render_template, request, flash

app = Flask(__name__)

#app.secret_key = "manbearpig_MUDMAN888"
apikey=os.environ.get('API_KEY')
apisecret=os.environ.get('API_SECRET')
qty=0.001#os.environ.get('QTY_ORDER')
tp=1.5#os.environ.get('TP')

client = Client(apikey, apisecret)
exchange = ccxt.binance({
    'apiKey': apikey,
    'secret': apisecret,
    'enableRateLimit': True,
    # 'options': {'adjustForTimeDifference': True}
})
exchange.load_markets()


def orderBuy(quantity, symbol, order_price):
    try:
        #order = client.order_limit_buy(
        #    symbol=symbol,
        #    quantity=quantity,
        #    price=order_price)
        order=client.order_market_buy(
            symbol=symbol,
            quantity=quantity
        )
        print(order)
        response=True
    except Exception as e:
        print("An exception occured - {}".format(e))
        return False
    return response

def orderSell(quantity, symbol, order_price):
    try:
        #order = client.order_limit_sell(
        #    symbol=symbol,
        #    quantity=quantity,
        #    price=order_price)
        order=client.order_market_sell(
            symbol=symbol,
            quantity=quantity
        )
        print(order)
        response=True
    except Exception as e:
        print("An exception occured - {}".format(e))
        return False
    return response  
@app.route('/')
def welcome():
    return "<h1>Questo è il trading bot di ASTRID</h1>"

@app.route("/hello")
def index():
	flash("Qual'è il tuo nome?")
	return render_template("index.html")

@app.route("/greet", methods=['POST', 'GET'])
def greeter():
	flash("Hi " + str(request.form['name_input']) + ", great to see you!")
	return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():

    data = json.loads(request.data)

    if data['passphrase'] != os.environ.get('WEBHOOK_PASSPHRASE'):
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }
    side = data['strategy']['order_action'].upper()
    quantity = float(qty) #0.001  data['strategy']['order_contracts']
    ticker = data['ticker'].upper()
    ticker='BTCUSDT'
    order_price = round(data['strategy']['order_price'],2)
    
    

    if side == 'BUY':
          order_response = orderBuy(quantity,ticker, order_price)
       
    else:
          order_response = orderSell(quantity,ticker, order_price)
   

    if order_response:
        return {
            "code": "success",
            "message": "Order executed."
        }
    else:
        print("Order Failed.")

        return {
            "code": "error",
            "message": "Order Failed."
        }
