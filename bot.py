import numpy
import websocket, json, pprint
import ta
from binance.client import Client   
import config
SOCKET ="wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSDT'
TRADE_QUANTITY = 0.05
in_position = False
closes = []

client = Client(config.API_KEY,config.SECRET_KEY,tld = 'us')

def order(side,quantity,symbol,order_type = ORDER_TYPE_MARKET ):
    try:
        print("sending order")
        order = client.create_order(symbol = symbol,side = side, quantity = quantity, type=order_type)
        print(order)
    except Exception as e:
        return False
    return False

def on_open(ws):
    print('opened')
    
def on_close(ws):
    print('closed')
    
def on_message(ws,message):
    global closes
    json_message = json.loads(message)
    pprint.pprint(json_message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("close")
        print(closes)
        if len(closes) > RSI_PERIOD:
            np_closes = numpy(closes)
            rsi = ta.momentum.rsi(np_closes,windows = RSI_PERIOD)
            print("all rsi")
            print(rsi)
            last_rsi = rsi[-1]
            print("The current rsi is: {}".format(last_rsi))
            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Selllllll")
                    order_succeeded = order(SIDE_SELL,TRADE_QUANTITY,TRADE_SYMBOL)
                    ##logic biannce
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("Have enought")
                print("Buyyyyyyy")
                
                # logic binance
ws = websocket.WebSocketApp(SOCKET,on_open=on_open , on_close=on_close, on_message=on_message )
ws.run_forever()
