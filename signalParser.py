from binance_api import check_if_trade_exist


def signalParser(message): 
    try:
        from binance_api import create_order
        
        # Your trade message
        trade_message=message
        import re
        # Extracting entry price
        entry_price_match = re.search(r'Entry:\s*([\d.]+)', trade_message)
        entry_price = float(entry_price_match.group(1)) if entry_price_match else None

        # Extracting symbol
        symbol_match = re.search(r'#(\w+)', trade_message)
        symbol = symbol_match.group(1) if symbol_match else None

        # Determine trade direction (short or long)
        trade_direction_match = re.search(r'Short|Long', trade_message)
        trade_direction = trade_direction_match.group() if trade_direction_match else None

        # Extracting leverage
        leverage_match = re.search(r'Leverage:\s*([\d.]+)\s*x', trade_message)
        leverage = float(leverage_match.group(1)) if leverage_match else None

        # Find the stop-loss section
        stop_loss_section_match = re.search(r'⛔ Stop-Loss:([\s\S]+?)(?=\w+:|$)', trade_message)
        stop_loss_section = stop_loss_section_match.group(1).strip() if stop_loss_section_match else ""

        # Extracting stop-loss price (SP)
        sp_match = re.search(r'([\d.]+)', stop_loss_section)
        sp = float(sp_match.group(1)) if sp_match else None

        # Extracting target prices
        targets_match = re.findall(r'Target \d:\s*([\d.]+)', trade_message)
        targets = [float(target) for target in targets_match] if targets_match else None
        if sp==None:

            sp=entry_price/leverage
            sp=entry_price-sp
        # Print the extracted values
        print("Symbol:", symbol)
        print("Entry Price:", entry_price)
        print("Trade Direction:", trade_direction)
        print("Leverage:", leverage)
        print("Stop-Loss (SP):", sp)
        print("Target Prices:", targets)
        if(check_if_trade_exist(symbol)):
            return create_order(symbol=symbol,side=trade_direction,leverage=leverage,sp=sp,tk1=targets[0],tk2=targets[1],tk3=targets[2],tk4=targets[3],entryPrice=entry_price),
        else:
            (False,"already have active trade with same signal")
    except:
        return (False,"no signal in message")
    