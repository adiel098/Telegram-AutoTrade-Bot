import configparser
import json
import os
import sys
from datetime import datetime
from database  import *
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')
import ccxt
def read_config(file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config
config = read_config()
binance = ccxt.binanceusdm({
        'apiKey': config.get('BINANCE', 'api_key'),
        'secret': config.get('BINANCE', 'api_secret'),
        'verbose': False,  # switch it to False if you don't want the HTTP log
    })
amountDollarPerOrder=float(config.get('SETTING', 'amountPerTrade'))

def getBalance():
    
    coinsBalance=binance.fetch_balance()
    strBalances="\n"
        
    for k, v in coinsBalance["USDT"].items():
        if(k=='free'):
            strBalances=strBalances+"Free to use:"+" "+str("%.2f" %v)+"$"+'\n'
        if(k=='used'):
            strBalances=strBalances+"Currently in use:"+" "+str("%.2f" %v)+"$"+'\n\n'
        if(k=='total'):
            strBalances=strBalances+"Total:"+" "+str("%.2f" %v)+"$"+'\n'
             

    return strBalances
def getOpenedPosition():
    file1 = open("SymbolsTraded.txt","r")
    symbolsTraded=file1.readlines()
    positions = binance.fetchPositions()
    for i,line in enumerate(symbolsTraded):
        symbolsTraded[i]=line.strip()
    positionsDetails=[]
    text=""
    for symbol1 in symbolsTraded:
        if(get_trade_db(symbol1)!=None):
            date,symbol,leverage,entryPrice,position,amount,sp,tk1,tk2,tk3,tk4,active,status=get_trade_db(symbol1)

            for k in positions:
                if(float(k["info"]["positionAmt"])!=0 and symbol1==k["info"]["symbol"]) :
                    markPrice=float(k["info"]["markPrice"])
                    markPrice=float("%.6f" %markPrice)
                    entryPrice=float("%.6f" %entryPrice)
                    unRealizedProfit=float(k["info"]["unRealizedProfit"])
                    unRealizedProfit=float("%.2f" %unRealizedProfit)
                    percentage=float(k["percentage"])
                    tk1=float("%.6f" %tk1)
                    tk2=float("%.6f" %tk2)
                    tk3=float("%.6f" %tk3)
                    sp=float("%.6f" %sp)
                    if(amount>10):
                        amount=float("%.2f" %amount)
                    elif(amount<0):
                        amount=float("%.5f" %amount)
                    else:
                        amount=float("%.3f" %amount)

                    positionsDetails.append({date,symbol,status,position,leverage,amount,entryPrice,tk1,tk2,tk3,markPrice,sp,unRealizedProfit,percentage})
            if positionsDetails:
                text=text+ f"{date}\n\n 🎛Symbol: #{symbol}\n 📈 Position: {position}\n 🏦Leverage: {leverage}\n ▶️Entry Price: {entryPrice}\n ⏩Mark Price: {markPrice}\n 🎒Amount: {amount}\n\n 📊Status: {status}\n 🔹Target 1: {tk1}\n 🔹Target 2: {tk2}\n 🔹Target 3: {tk3}\n ⛔️Stop-Loss: {sp}\n\n 💰Profit: {unRealizedProfit}$\n 🎚Percentage: {percentage}%\n ----------------------\n"

            else:
                text="You dont have live position now."
    return text
def getStats():
    
    file1 = open("SymbolsTraded.txt","r")
    symbolsTraded=file1.readlines()
    for i,line in enumerate(symbolsTraded):
        symbolsTraded[i]=line.strip()
    file2 = open("UserInformation.txt","r")
    date=file2.read()
    fetchTrades=[]
    profitPNL=0 
    winTrades=0
    loseTrades=0
    symbolsCounts=0
    startDate = datetime.fromtimestamp(int(float(date)/1000)).strftime('%d/%m/%y')
    dateNow= datetime.today().strftime('%d/%m/%y')

    for symbol in symbolsTraded:
        fetchTrades.append( binance.fetchMyTrades(symbol=symbol,since=int(float(date))))
    for symbol in fetchTrades:
        symbolsCounts+=1
        for trade in symbol:
            if(float(trade["info"]["realizedPnl"])>0):
                winTrades+=1
            if(float(trade["info"]["realizedPnl"])<0):
                loseTrades+=1
            profitPNL=profitPNL+float(trade["info"]["realizedPnl"])

    profitPNL="%.2f" %profitPNL
    countTrades=winTrades+loseTrades 
    winPrecentage=("%.2f" % ((winTrades/countTrades)*100))

    return f" *📊Trading Stats*\n 📆{startDate} - {dateNow} \n\n ♠️Tokens Traded: {symbolsCounts}\n ♻️Total Trades: {countTrades}\n ✅Winners: {winTrades}\n ❌Losers: {loseTrades}\n\n 🎚Signals Win Rate: {winPrecentage}%\n💰Total Profit: {profitPNL}$\n "
def create_order(symbol,entryPrice,side,leverage,sp,tk1,tk2,tk3,tk4):    
    if check_free_usdt():
                    amount=(amountDollarPerOrder/entryPrice)*leverage
                    if("Long" in side):
                        side="buy"
                        side2="sell"
                    elif("Short" in side):
                        side="sell"
                        side2="buy" 
                    binance.set_leverage(symbol=symbol,leverage=int(leverage))
                    
                    market_buy_order = binance.create_order(symbol, "LIMIT",side=side, amount=amount,price=entryPrice, params={'reduceOnly': False})
                    sl_order = binance.create_order(symbol, "STOP_MARKET", side2, amount=amount, params={"stopPrice": sp, 'reduceOnly': True, 'timeInForce': 'GTC'})
                    tp1_order = binance.create_order(symbol,"TAKE_PROFIT",price=tk1, side=side2,amount=amount/2, params={"stopPrice": tk1,'reduceOnly': True, 'timeInForce': 'GTC'})
                    tp2_order = binance.create_order(symbol,"TAKE_PROFIT",price=tk2, side=side2,amount=amount/4, params={"stopPrice": tk2,'reduceOnly': True, 'timeInForce': 'GTC'})
                    tp3_order = binance.create_order(symbol,"TAKE_PROFIT",price=tk3, side=side2,amount=amount/4, params={"stopPrice": tk3,'reduceOnly': True, 'timeInForce': 'GTC'})
                    new_trade_db(price=float(entryPrice),date=str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),symbol=symbol,leverage=float(leverage),qty=float(amount),positionSide=side,stoploss=float(sp),tk1=float(tk1),tk2=float(tk2),tk3=float(tk3),tk4=float(tk4),ordersID=json.dumps([market_buy_order["info"]["orderId"],sl_order["info"]["orderId"],tp1_order["info"]["orderId"],tp2_order["info"]["orderId"],tp3_order["info"]["orderId"]]))
                    check_and_update_unique_names("SymbolsTraded.txt",symbol)
                    print("Create ALL Orders and DB insert Successs")

                    return True,{"symbol":symbol,"leverage":leverage,"amount":amount,"side":side}
                   
                    
    else:
                print("you dont have enuogh money")
                return False 
def check_and_update_unique_names(filename,symbol):
    file1 = open("SymbolsTraded.txt","a")
    file1.write("\n"+symbol)
    file1.close()
    try:
        # Read existing names from the file
        with open(filename, 'r') as file:
            existing_names = file.read().splitlines()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return

    # Use a set to check for duplicates
    unique_names = set()
    duplicates = set()

    for name in existing_names:
        if name in unique_names:
            duplicates.add(name)
        else:
            unique_names.add(name)

    if  duplicates:
        unique_names_list = list(unique_names)

        # Write the list of unique names back to the file
        with open(filename, 'w') as file:
            file.write('\n'.join(unique_names_list))
def update_stoploss_order(lastOrderID,symbol,newSP,position,amount):
        try:
            try:
                binance.cancel_order(str(lastOrderID), symbol)
                print("updateStoplossOrder cancel sp order before new sp order, Success")
            except:
                print("updateStoplossOrder cancel sp order before new sp order, Failed")
            try:
                sl_order = binance.create_order(symbol, "STOP_MARKET", position, amount=amount, params={"stopPrice": newSP, 'reduceOnly': True, 'timeInForce': 'GTC'})
                sl_order_id=sl_order["id"]
                print("create new sp order , Success")
            except:
                print("create new sp order , Failed")
            update_stoploss_order_id_db(newOrderID=sl_order_id,symbol=symbol)

            update_trade_stoploss_db(symbol=symbol,newSP=newSP)
            print("updateStoplossOrder method,Failed")
        except:
            print("updateStoplossOrder method,Failed")
def cancel_Stoploss_order(symbol):
        orderid=get_orders_id_db(symbol=symbol)
        orderid=orderid[1]
        try:
            binance.cancel_order(orderid, symbol)
            print("cancelStoplossOrder Success")
        except:
               print("cancelStoplossOrder Failed")
def check_free_usdt(symbol):
    coinsBalance=binance.fetch_balance()
    freeUSDT=float(coinsBalance["USDT"]["free"])
    lastSymbolPrice=binance.fetch_ticker(symbol)
    lastSymbolPrice=float(lastSymbolPrice["last"])
    return(freeUSDT>amountDollarPerOrder)
def check_order_filled(symbol,type):
    orderID=(get_orders_id_db(symbol=symbol))
    if(type=="limit"):

        return binance.fetch_order_status(id=orderID[0],symbol=symbol) == 'closed'
    if(type=="stoploss"):
        return binance.fetch_order_status(id=orderID[1],symbol=symbol) == 'closed'    
    if(type=="tk1"):
        return binance.fetch_order_status(id=orderID[2],symbol=symbol) == 'closed'
    if(type=="tk2"):
        return binance.fetch_order_status(id=orderID[3],symbol=symbol) == 'closed'
    if(type=="tk3"):
        return binance.fetch_order_status(id=orderID[4],symbol=symbol) == 'closed'        
def get_trade_price(symbol):
    orderID=(get_orders_id_db(symbol=symbol))
    price=binance.fetch_order(id=orderID[0],symbol=symbol)
    price=price["info"]["avgPrice"]
    return price
def check_if_trade_exist(symbol):
    return symbol not in get_active_trades_symbols_db()
