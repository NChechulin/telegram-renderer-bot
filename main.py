import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

expect = None


def get_token():
    with open('token.txt', 'r') as f:
        return f.read().strip()

    raise Exception("Unable to read token from file token.txt")


# Comand handlers
def first_message(update, context):
    """Send a greeting message when /start or /help message is sent"""

    response = "Hi! I am Renderer Bot. I can render LaTeX and Markdown code. Type /latex to render LaTex or /md to render Markdown"
    update.message.reply_text(response)


def text(update, context):
    global expect

    if expect == 'latex':
        update.message.reply_text('TODO: compile LaTeX')
        expect = None
    elif expect == 'markdown':
        update.message.reply_text('TODO: compile Markdown')
        expect = None


def latex(update, context):
    global expect
    update.message.reply_text('Send your LaTeX code')
    expect = 'latex'


def markdown(update, context):
    global expect
    update.message.reply_text('Send your Markdown code')
    expect = 'markdown'


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"',markdown
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(get_token(), use_context=True)

    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", first_message))
    dp.add_handler(CommandHandler("help", first_message))
    dp.add_handler(CommandHandler("latex", latex))
    dp.add_handler(CommandHandler("markdown", markdown))
    dp.add_handler(CommandHandler("md", markdown))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, text))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
