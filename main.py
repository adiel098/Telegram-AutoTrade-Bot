

from binance_api import getBalance,getOpenedPosition,getStats
from telegram import  Update,Bot
import configparser

from web_socket_trades import *
from signalParser import signalParser

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,)
# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
BALANCE, LIVE_TRADES, STATS= range(3)
def read_config(file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config
config = read_config()

bot_token = config.get('TELEGRAM', 'bot_token')
target_chat_id = config.get('TELEGRAM', 'target_channel')
botOwner=config.get('TELEGRAM', 'owner_id')
bot = Bot(token=bot_token)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    import os
    if os.path.isfile("./UserRegisterDate.txt"):
        print("User already exist")
    else:
        from datetime import datetime
        import time
        file1 = open("UserRegisterDate.txt","a")
        file1.write(str(((time.time())-24*60*60)*1000))
        file1.close()
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("💰Balance", callback_data=str(BALANCE)),],
        [InlineKeyboardButton("🌐Live Trades", callback_data=str(LIVE_TRADES)),],
        [InlineKeyboardButton("📊Stats", callback_data=str(STATS)),],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text('''🚀 *Welcome to Autodictum \nYour Ultimate AutoTrading Bot!* 🤖💹\n\n Get ready for an incredible trading experience powered by Predictum signals! 📈✨\n\n✅ Auto-trade with precision\n💼 Diversify your portfolio\n📊 Real-time updates\n\n💡 Smart features: Intuitive controls, risk management, and more for savvy trading.\n''',parse_mode='Markdown', reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🌐Live Trades", callback_data=str(LIVE_TRADES)),],
        [InlineKeyboardButton("📊Stats", callback_data=str(STATS)),],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="*Here you able to see your #USDT balance on your Binance account* 🤑"+'\n'+getBalance(), reply_markup=reply_markup,parse_mode="Markdown"
    )
    return START_ROUTES


async def openedposition(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("💰Balance", callback_data=str(BALANCE)),],
        [InlineKeyboardButton("📊Stats", callback_data=str(STATS)),],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
   
    text="*Live Trades*\n ----------------------\n"
    for i in getOpenedPosition():
            text=text+i.__str__()
    text="You not have access because your investments under 5k$"
    await query.edit_message_text(text=text,parse_mode='Markdown', reply_markup=reply_markup)
   
    return START_ROUTES



async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("💰Balance", callback_data=str(BALANCE)),],
        [InlineKeyboardButton("🌐Live Trades", callback_data=str(LIVE_TRADES)),],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
        # Initial display of stats
    text = getStats()
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')
        


    return START_ROUTES



async def readmessages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            result = update.channel_post.text
            success=signalParser(result)
            if(success[0]):
                symbol=success[0][1]["symbol"]
                leverage=success[0][1]["leverage"]
                side=success[0][1]["side"]

            
                await bot.send_message(chat_id=target_chat_id, text=f"📣*New Trade!* \n\n 🎛Symbol: #{symbol}\n 🏦Leverage: {leverage}\n 📈Position: {side}",parse_mode='Markdown')
            else:
                await bot.send_message(chat_id=target_chat_id, text="Trade Not Success ")
        except:
                await bot.send_message(chat_id=target_chat_id, text="Message not supported click /start to continue")
    

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    
    application = Application.builder().token(bot_token).build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START_ROUTES: [
            CallbackQueryHandler(balance, pattern="^" + str(BALANCE) + "$"),
            CallbackQueryHandler(openedposition, pattern="^" + str(LIVE_TRADES) + "$"),
            CallbackQueryHandler(stats, pattern="^" + str(STATS) + "$"),
        ],
    },
    fallbacks=[CommandHandler("start", start)],
)

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    application.add_handler(MessageHandler(filters.ALL, readmessages))

    # Run the bot until the user presses Ctrl-C
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == "__main__":


    main()


def read_config(file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config






    




