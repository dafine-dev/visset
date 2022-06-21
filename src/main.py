from configparser import ConfigParser
from visset.languages import Language
from visset.controllers import Controller
from flask import Flask, request
from telebot import TeleBot
from telebot.types import Update


if __name__ == "__main__":
    config = ConfigParser()
    config.read('application.conf')

    TOKEN = config['api']['token']
    URL = config['server']['url']

    bot = TeleBot(TOKEN)
    from visset import endpoints

    server = Flask(__name__)

    @server.route('/' + TOKEN, methods=['POST'])
    def getMessage():
        bot.process_new_updates([Update.de_json(request.stream.read().decode('utf-8'))])
        return "!", 200

    @server.route('/')
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=URL + TOKEN)
        return "!", 200

    Language.start()
    Controller()
    server.run()
