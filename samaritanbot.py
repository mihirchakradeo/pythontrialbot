from nltk.corpus import wordnet
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import praw
import urllib2
import json

user_agent = ("Google Chrome")

r = praw.Reddit(user_agent = user_agent)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello!')


def help(bot, update):
    if update.message.text[6:]=='reddit':
        bot.sendMessage(update.message.chat_id, text='Usage: /reddit <search query>\nExample usage: /reddit python to search about python')

    elif update.message.text[6:]=='define':
        bot.sendMessage(update.message.chat_id, text='Usage: /define <define term>\nExample usage: /define word to get the dictionary meaning of word')

    elif update.message.text[6:]=='fact':
        bot.sendMessage(update.message.chat_id, text='Usage: /fact <trivia/math/date>\nExample usage: /fact math to get a random fact about math')



def redditfun(bot, update):
    bot.sendMessage(update.message.chat_id, text="Retrieving "+update.message.text[8:].upper())
    subreddit = r.get_subreddit(update.message.text[8:])
    
    try:
        for submission in subreddit.get_hot(limit = 1):
            bot.sendMessage(update.message.chat_id, text="Title: "+submission.title)
            bot.sendMessage(update.message.chat_id, text=submission.selftext)
            bot.sendMessage(update.message.chat_id, text="URL: "+submission.url)
            bot.sendMessage(update.message.chat_id, text="Score: "+`submission.score`)

    except Exception, e:
        if ("%s"%e) == 'SUBREDDIT_NOEXIST':
            bot.sendMessage(update.message.chat_id, text="Thread does not exist!")

def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text[6:].upper())


def fact(bot, update):
    if update.message.text[6:]=='trivia':
        url = urllib2.urlopen('http://numbersapi.com/random/trivia')
        result = url.read()
        htmlstr = result.decode()
        bot.sendMessage(update.message.chat_id, text=htmlstr)

    elif update.message.text[6:]=='math':
        url = urllib2.urlopen('http://numbersapi.com/random/math')
        result = url.read()
        htmlstr = result.decode()
        bot.sendMessage(update.message.chat_id, text=htmlstr)

    elif update.message.text[6:]=='date':
        url = urllib2.urlopen('http://numbersapi.com/random/date')
        result = url.read()
        htmlstr = result.decode()
        bot.sendMessage(update.message.chat_id, text=htmlstr)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
    bot.sendMessage(update.message.chat_id, text="%s" %(error))


def definition(bot, update):
    try:
        synsets = wordnet.synsets(update.message.text[8:])[0].definition()
        bot.sendMessage(update.message.chat_id, text=synsets)
        
    except Exception, e:
        bot.sendMessage(update.message.chat_id, text="Word doesn't exist!")
    


def main():
    # Create the EventHandler and pass it your bot's token.
    fp = open("token.txt", 'r')
    token = fp.read()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("echo", echo))
    dp.add_handler(CommandHandler("reddit", redditfun))
    dp.add_handler(CommandHandler("define", definition))
    dp.add_handler(CommandHandler("fact", fact))

    #OLD BOT METHOD
    #dp.add_handler(MessageHandler([Filters.text], redsearch))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()