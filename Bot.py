from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging


class Bot:

    def __init__(self, token):
        self.TOKEN = token
        self.updater = Updater(token=self.TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def start(self, handler_bienvenida):
        self.dispatcher.add_handler(handler_bienvenida)
        self.updater.start_polling()

    def add_handler(self, handler):
        self.dispatcher.add_handler(handler)

