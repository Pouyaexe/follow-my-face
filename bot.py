import openai
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

import logging

# Configure logging for the bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Set your OpenAI API key
openai.api_key = "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"

# Define the conversation states
SEND_MESSAGE = 1

# Define a function that prompts the user to enter a message
def send_message(bot, update):
    # Log the message that the bot received
    # logging.info("Received message: %s" % update.message.text)

    # Create a keyboard with a single button to submit the message
    keyboard = [['Send message']]
    reply_markup = ReplyKeyboardMarkup(keyboard)

    # Prompt the user to enter a message
    update.message.reply_text("Please enter a message for the chatbot:", reply_markup=reply_markup)

    # Move to the next conversation state
    return SEND_MESSAGE

# Define a function that sends the user's message to the chatbot and displays the response
def send_message(bot, update):
    # Log the message that the bot received
    logging.info("Received message: %s" % update.effective_message.text)

    # Create a keyboard with a single button to submit the message
    keyboard = [['Send message']]
    reply_markup = ReplyKeyboardMarkup(keyboard)

    # Prompt the user to enter a message
    update.effective_message.reply_text("Please enter a message for the chatbot:", reply_markup=reply_markup)

    # Move to the next conversation state
    return SEND_MESSAGE

# Set up the Telegram bot to respond to the "/chatbot" command
updater = Updater("5776863971:AAERKuZgOuu0MtehJ1veynxTz741G7sS5nY")
dispatcher = updater.dispatcher

# Set up the conversation handler
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('chatbot', send_message)],
    states={
        SEND_MESSAGE: [MessageHandler(Filters.regex('^Send message$'), send_message_to_chatbot)]
    },
    fallbacks=[]
)

dispatcher.add_handler(conversation_handler)

# Start the bot
updater.start_polling()
