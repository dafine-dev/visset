from configparser import ConfigParser
from telebot import TeleBot


if __name__ == '__main__':
    config = ConfigParser()
    config.read('application.conf')

    bot = TeleBot(config['api']['token'])

    from visset import endpoints
    from visset.controllers import Controller
    from visset.languages import Language

    Language.start()
    Controller()
    bot.polling()
