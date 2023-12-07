import json
import sqlite3
con = sqlite3.connect('Trades.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS Trades
               (id INTEGER PRIMARY KEY,date text, symbol text,leverage float, position text, qty float, price float, stoploss float, tk1 flaot,tk2 float,tk3 float,tk4 float,status text,active text, ordersID text)''')  
def new_trade_db(date,symbol,leverage,price,positionSide,qty,stoploss,tk1,tk2,tk3,tk4,ordersID):
    con = sqlite3.connect('Trades.db')
    cur = con.cursor()
    try:
        con.execute('''INSERT INTO Trades (date,symbol,leverage,position,qty,price,stoploss,tk1,tk2,tk3,tk4,status,active,ordersID)
        VALUES (?, ?,?,?,?,?,?,?,?,?,?,'NEW','YES',?)''',(date,symbol,leverage,positionSide,qty,price,stoploss,tk1,tk2,tk3,tk4,ordersID))    
        print("New Trade inserted to DB, Successfull.")
        con.commit()
        con.close()

        return True

    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
        con.commit()
        con.close()

        return False
def get_active_trades_symbol_db():
    select_query = '''
    SELECT symbol FROM Trades
    WHERE active = 'YES'; 
    '''
    symbols=[]
    # Try to execute the query
    try:
        cur.execute(select_query)
        # Fetch all the results
        symbol_values = cur.fetchall()
        # Print or use the retrieved values
        for symbol in symbol_values:
            symbols.append(symbol[0].lower())
    except sqlite3.Error as e:
        print(f"Error executing SELECT query: {e}")

    # Close the connection
    con.commit()
    con.close()
    return symbols
def get_trade_db(symbol):
    con = sqlite3.connect('Trades.db')
    cur = con.cursor()
    select_query = '''
    SELECT date,symbol,leverage,price,position,qty,stoploss,tk1,tk2,tk3,tk4,active,status FROM Trades
    WHERE symbol=? AND active = 'YES' ; 
    '''    
    # Try to execute the query
    try:
        cur.execute(select_query,[symbol])
        # Fetch all the results
        symbol_values = cur.fetchall()        
    except sqlite3.Error as e:
            print(f"Error executing SELECT query: {e}")
        # Close the connection
    con.commit()
    con.close()
    if symbol_values:
        return symbol_values[0]
    return None
def update_trade_status_db(symbol,newStatus):
    conn = sqlite3.connect('Trades.db')
    cursor = conn.cursor()

    # Update the "status" column where "symbol"  and "active" is "yes"
    update_query = '''
    UPDATE Trades
    SET status = ?
    WHERE symbol = ? AND active = 'YES';
    '''

    # Try to execute the update query
    try:
        cursor.execute(update_query,[newStatus,symbol])
        print(f"Update Status to {newStatus} in symbol: {symbol} ,successful.")
    except sqlite3.Error as e:
        print(f"Error updating data: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def update_trade_stoploss_db(symbol,newSP):


    conn = sqlite3.connect('Trades.db')
    cursor = conn.cursor()

    # Update the "stoploss" column where "symbol"  and "active" is "yes"
    update_query = '''
    UPDATE Trades
    SET stoploss = ?
    WHERE symbol = ? AND active = 'YES';
    '''

    # Try to execute the update query
    try:
        cursor.execute(update_query,[newSP,symbol])
        print("Update Stoploss Price in DB successful.")
    except sqlite3.Error as e:
        print(f"Error updating data: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def set_trade_noActive_db(symbol):

    
    conn = sqlite3.connect('Trades.db')
    cursor = conn.cursor()

    # Update the "active" column where "symbol"  and "active" is "yes"
    update_query = '''
    UPDATE Trades
    SET active = 'NO'
    WHERE symbol = ? AND active = 'YES';
    '''

    # Try to execute the update query
    try:
        cursor.execute(update_query,[symbol])
        print("Update Active to 'NO' successful.")
    except sqlite3.Error as e:
        print(f"Error updating data: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def update_stoploss_order_id_db(newOrderID,symbol):


    conn = sqlite3.connect('Trades.db')
    cursor = conn.cursor()

    # Update the "stoploss" column where "symbol"  and "active" is "yes"
    update_query = '''
    UPDATE Trades
    SET ordersID = ?
    WHERE symbol = ? AND active = 'YES';
    '''
    orders=get_orders_id_db(symbol=symbol)
    orders[1]=newOrderID
    orders=json.dumps(orders)
    # Try to execute the update query
    try:
        cursor.execute(update_query,[orders,symbol])
        print("Update Stoploss Order ID successful.")
    except sqlite3.Error as e:
        print(f"Error updating data: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def get_trade_amount_db(symbol):
    con = sqlite3.connect('Trades.db')
    cur = con.cursor()
    result=""
    query = f"SELECT qty FROM Trades WHERE symbol = ? AND active = ?"
   
    # Try to execute the query
    try:
        cur.execute(query,[symbol,'YES'])
        # Fetch all the results
        result = cur.fetchone()
    except sqlite3.Error as e:
            print(f"Error executing SELECT query: {e}")
        # Close the connection
    con.commit()
    con.close()
    return str("%.5f" %result[0])
def get_orders_id_db(symbol):
    con = sqlite3.connect('Trades.db')
    cur = con.cursor()
    result=""
    query = f"SELECT ordersID FROM Trades WHERE symbol = ? AND active = ?"
   
    # Try to execute the query
    try:
        cur.execute(query,[symbol,'YES'])
        # Fetch all the results
        result = cur.fetchone()
    except sqlite3.Error as e:
            print(f"Error executing SELECT query: {e}")
        # Close the connection
    con.commit()
    con.close()
    output_list = json.loads(str(result[0]))
    
    return output_list  
def update_trade_enteryprice_db(symbol,realPrice):

    conn = sqlite3.connect('Trades.db')
    cursor = conn.cursor()

    # Update the "status" column where "symbol"  and "active" is "yes"
    update_query = '''
    UPDATE Trades
    SET price = ?
    WHERE symbol = ? AND active = 'YES';
    '''

    # Try to execute the update query
    try:
        cursor.execute(update_query,[realPrice,symbol])
        print("Update EntryPrice successful.")
    except sqlite3.Error as e:
        print(f"Error updating data: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def update_trade_amount_db(symbol,amount):
    
    conn = sqlite3.connect('Trades.db')
    cursor = conn.cursor()

    # Update the "status" column where "symbol"  and "active" is "yes"
    update_query = '''
    UPDATE Trades
    SET qty = ?
    WHERE symbol = ? AND active = 'YES';
    '''

    # Try to execute the update query
    try:
        cursor.execute(update_query,[amount,symbol])
        print("Update Amount successful.")
    except sqlite3.Error as e:
        print(f"Error updating data: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    return amount
def get_active_trades_symbols_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('Trades.db')
    cursor = conn.cursor()

    # Retrieve active trades from the database
    cursor.execute("SELECT * FROM Trades WHERE ACTIVE = 'YES'")
    active_trades = cursor.fetchall()

    # Get a list of symbols with active trades
    symbols_with_active_trades = [trade[2] for trade in active_trades]  # Assuming the symbol is in the second column, modify accordingly

    # Close the database connection
    conn.close()
    return symbols_with_active_trades
