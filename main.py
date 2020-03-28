import latex
import logging
import md
import telegram
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


def send_document(user, file_path):
    telegram.User.send_document(user, document=open(file_path, 'rb'))


# Comand handlers
def first_message(update, context):
    """Send a greeting message when /start or /help message is sent"""

    response = "Hi! I am Renderer Bot. I can render LaTeX and Markdown code. Type /latex to render LaTex or /md to render Markdown"
    update.message.reply_text(response)


def text(update, context):
    global expect

    # TODO: Add messages if file was incorrect
    # TODO: Add file support

    if expect == 'latex':
        user = update.message.from_user

        pdf_path = latex.render(update.message.text)

        send_document(user, pdf_path)

        update.message.reply_text('PDF was generated')
        expect = None
    elif expect == 'markdown':
        user = update.message.from_user

        pdf_path = md.render(update.message.text)
        send_document(user, pdf_path)

        update.message.reply_text('PDF was generated')
        expect = None


def latex_command(update, context):
    global expect
    update.message.reply_text('Send your LaTeX code')
    expect = 'latex'


def markdown_command(update, context):
    global expect
    update.message.reply_text('Send your Markdown code')
    expect = 'markdown'


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(get_token(), use_context=True)

    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", first_message))
    dp.add_handler(CommandHandler("help", first_message))
    dp.add_handler(CommandHandler("latex", latex_command))
    dp.add_handler(CommandHandler("markdown", markdown_command))
    dp.add_handler(CommandHandler("md", markdown_command))

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
