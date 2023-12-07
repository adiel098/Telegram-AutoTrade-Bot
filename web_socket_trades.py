import websocket
import json
from database import get_active_trades_symbol_db
from trades_controller import controll
def on_message(ws, message):
    symbols = get_active_trades_symbol_db()
    data = json.loads(message)
    for v in data: 
        if str(v['s']).lower() in symbols:
            symbol_name=str(v['s'])
            current_price = str(v['c'])
            print(symbol_name+" "+str(current_price))
            controll(symbol=symbol_name,lastPrice=float(current_price))

   
    
    

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    # Subscribe to the real-time price updates for the given symbol
   
     ws.send(json.dumps({"method": "SUBSCRIBE", "params": ["!ticker@arr"], "id": 1}))

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://fstream.binance.com/ws", on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    ws.close()