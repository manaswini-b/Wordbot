import enchant
from telegram.ext import Updater
updater = Updater(token='TOKEN') #Replace the 'TOKEN' with the token obtained for your bot
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please enter a word and I will suggest the similar words!")
from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
d = enchant.Dict("en")
def reply(bot, update):
	temp=update.message.text
	if not (temp.startswith("Suggeste")):
		response = "Suggested: "
		print (str(temp))
		tmp = d.suggest(str(temp))
		for i in tmp:
			response += i+" , "
	bot.sendMessage(chat_id=update.message.chat_id, text=response[:-3])
from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler([Filters.text], reply)
dispatcher.add_handler(echo_handler)
def caps(bot, update, args):
	text_caps = ' '.join(args).upper()
	bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)
caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)
from telegram import InlineQueryResultArticle, InputTextMessageContent
def inline_caps(bot, update):
	query = update.inline_query.query
	if not query:
		return
	results = list()
	results.append(InlineQueryResultArticle(id=query.upper(),title='Caps',input_message_content=InputTextMessageContent(query.upper())))
	bot.answerInlineQuery(update.inline_query.id, results)
from telegram.ext import InlineQueryHandler
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)
def unknown(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
unknown_handler = MessageHandler([Filters.command], unknown)
dispatcher.add_handler(unknown_handler)