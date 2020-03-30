"""Main file which starts the bot and sets all of the parameters"""

from bot import Bot

if __name__ == '__main__':
    bot = Bot('token.txt')
    bot.start()
