import telegram
from telegram.ext import Updater, CommandHandler

# Replace "YOUR_API_TOKEN" with your API token
bot = telegram.Bot(token="5776863971:AAERKuZgOuu0MtehJ1veynxTz741G7sS5nY")

updater = Updater(bot=bot)

# This function will be called whenever the user sends a message to the bot
def echo(update, context):
    # Get the user's message
    message = update.message.text
    
    # Convert the message to uppercase
    message = message.upper()
    
    # Send the message back to the user
    update.message.reply_text(message)

# This command handler will respond to the user's "/start" message
start_handler = CommandHandler("start", echo)

# Add the command handler to the updater
updater.dispatcher.add_handler(start_handler)

# Start the updater
updater.start_polling()
