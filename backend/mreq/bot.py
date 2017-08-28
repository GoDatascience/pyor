import os
from typing import List, Dict

import itertools
from mrq.queue import Queue
from telegram import ReplyKeyboardMarkup
from telegram.bot import Bot
from telegram.ext import Updater, CommandHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.dispatcher import Dispatcher
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.update import Update
from telegram.user import User

from mreq.models import NotificationSubscriber
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
updater = Updater(TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None

SUBSCRIBING, UNSUBSCRIBING = range(2)


def start(bot: Bot, update: Update):
    update.message.reply_text() # TODO Explain and show all commands

def subscribe(bot: Bot, update: Update):
    known_queues: List[str] = Queue.all_known()

    reply_keyboard: List[List[str]] = _group(4, known_queues)

    update.message.reply_text("Hi! To start receiving updates, please select the queues you want to subscribe to"
                              " and press 'Finish' when you're done.",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SUBSCRIBING


def subscribe_select_queue(bot: Bot, update: Update, user_data: Dict):
    answer: str = update.message.text

    if answer == "Finish":
        pass


    queues: List[str] = user_data.get("queues", [])
    queues.append(answer)
    user_data["queues"] = queues

    known_queues: List[str] = Queue.all_known()
    reply_keyboard: List[List[str]] = _group(4, known_queues)

    update.message.reply_text("Hi! To start receiving updates, please select the queues you want to subscribe to"
                              " and press 'Finish' when you're done.",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    chat_id: int = update.message.chat.id
    if not NotificationSubscriber.exists_chat_id(chat_id):
        subscriber = NotificationSubscriber(chat_id)
        if NotificationSubscriber.insert(subscriber):
            update.message.reply_text(
                "Ok! Now you're subscribed and you'll receive notifications when tasks starts and ends.")
            logger.info("New subscriber: %s" % chat_id)
    else:
        update.message.reply_text(
            "You're already subscribed.")

def unsubscribe(bot: Bot, update: Update):
    chat_id: int = update.message.chat.id
    if NotificationSubscriber.delete_chat_id(chat_id):
        update.message.reply_text(
            "Ok! You've unsubscribed and won't receive further notifications.")
    else:
        update.message.reply_text(
            "You weren't subscribed.")

def notify_subscribers(message: str):
    if not updater:
        return
    subscribers = NotificationSubscriber.find_all()
    for subscriber in subscribers:
        updater.bot.send_message(chat_id=subscriber.chat_id, text=message)


def _error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def run():
    if updater:
        dispatcher: Dispatcher = updater.dispatcher

        dispatcher.add_handler(ConversationHandler(
            entry_points=[CommandHandler("subscribe", subscribe)],
            states={
                SUBSCRIBING: [MessageHandler(Filters.text, subscribe_select_queue, pass_user_data=True)]
            }
        ))

        dispatcher.add_handler(CommandHandler("subscribe", subscribe))
        dispatcher.add_handler(CommandHandler("unsubscribe", unsubscribe))

        dispatcher.add_error_handler(_error)

        updater.start_polling()
        updater.idle()

def _group(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e != None] for t in itertools.zip_longest(*args))
