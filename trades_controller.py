from time import sleep
from binance_api import *
from database import *
def controll(symbol,lastPrice):
    date,symbol,leverage,entryPrice,position,amount,sp,tk1,tk2,tk3,tk4,active,status=get_trade_db(symbol)
        #SHORT position
    if(position=="sell"):
            #when new signal
                    if(status=='NEW'):
                        if(lastPrice>=entryPrice and check_order_filled(symbol=symbol,type="limit")):
                            update_trade_status_db(symbol,'FILLED')
                            realPrice=get_trade_price(symbol=symbol)
                            update_trade_enteryprice_db(symbol=symbol,realPrice=realPrice)
                            
                    if(status=='FILLED'):
                        if(lastPrice<=tk1 and check_order_filled(symbol=symbol,type="tk1")):
                            lastOrderID=get_orders_id_db(symbol)
                            lastOrderID=lastOrderID[1]
                            newAmount=update_trade_amount_db(symbol=symbol,amount=amount/2)
                            update_stoploss_order(lastOrderID,symbol,tk1,position,newAmount)
                            update_trade_status_db(symbol,'TK1')
    

                    elif(status=='TK1'):
                        if(lastPrice<=tk2 and check_order_filled(symbol=symbol,type="tk2")):
                            lastOrderID=get_orders_id_db(symbol)
                            lastOrderID=lastOrderID[1]
                            newAmount=update_trade_amount_db(symbol=symbol,amount=amount/2)
                            update_stoploss_order(lastOrderID,symbol,tk2,position,newAmount)
                            update_trade_status_db(symbol,'TK2')
                
                    elif(status=='TK2'):
                        if(lastPrice<=tk3 and check_order_filled(symbol=symbol,type="tk3")):
                            update_trade_status_db(symbol,'TK3')
                            set_trade_noActive_db(symbol)

                    if(lastPrice>=sp):
                        #SELL ALL POSITION
                        orders=get_orders_id_db(symbol=symbol)
                        tk1,tk2,tk3=orders[2],orders[3],orders[4]
                        if(status=='FILLED'):
                            binance.cancel_order(tk1, symbol)
                            binance.cancel_order(tk2, symbol)
                            binance.cancel_order(tk3, symbol)
                        if(status=='TK1'):
                            binance.cancel_order(tk2, symbol)
                            binance.cancel_order(tk3, symbol) 
                        if(status=='TK2'):
                            binance.cancel_order(tk3, symbol)      
                        update_trade_status_db(symbol=symbol,newStatus="STOP")
                        set_trade_noActive_db(symbol)
        #LONG position
    elif(position=="buy"):
            #when new signal
                    if(status=='NEW'):
                        if(lastPrice<=entryPrice and check_order_filled(symbol=symbol,type="limit")):
                            update_trade_status_db(symbol,'FILLED')
                            realPrice=get_trade_price(symbol=symbol)
                            update_trade_enteryprice_db(symbol=symbol,realPrice=realPrice)
                            
                    if(status=='FILLED'):
                        if(lastPrice>=tk1 and check_order_filled(symbol=symbol,type="tk1")):
                            lastOrderID=get_orders_id_db(symbol)
                            lastOrderID=lastOrderID[1]
                            newAmount=update_trade_amount_db(symbol=symbol,amount=amount/2)
                            update_stoploss_order(lastOrderID,symbol,tk1,position,newAmount)
                            update_trade_status_db(symbol,'TK1')
    

                    elif(status=='TK1'):
                        if(lastPrice>=tk2 and check_order_filled(symbol=symbol,type="tk2")):
                            lastOrderID=get_orders_id_db(symbol)
                            lastOrderID=lastOrderID[1]
                            newAmount=update_trade_amount_db(symbol=symbol,amount=amount/2)
                            update_stoploss_order(lastOrderID,symbol,tk2,position,newAmount)
                            update_trade_status_db(symbol,'TK2')
                
                    elif(status=='TK2'):
                        if(lastPrice>=tk3 and check_order_filled(symbol=symbol,type="tk3")):
                            update_trade_status_db(symbol,'TK3')
                            set_trade_noActive_db(symbol)

                    if(lastPrice<=sp):
                        #SELL ALL POSITION
                        orders=get_orders_id_db(symbol=symbol)
                        tk1,tk2,tk3=orders[2],orders[3],orders[4]
                        if(status=='FILLED'):
                            binance.cancel_order(tk1, symbol)
                            binance.cancel_order(tk2, symbol)
                            binance.cancel_order(tk3, symbol)
                        if(status=='TK1'):
                            binance.cancel_order(tk2, symbol)
                            binance.cancel_order(tk3, symbol) 
                        if(status=='TK2'):
                            binance.cancel_order(tk3, symbol)      
                        update_trade_status_db(symbol=symbol,newStatus="STOP")
                        set_trade_noActive_db(symbol)

