"""Main file which starts the bot and sets all of the parameters"""

import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from rendering import render_latex, render_markdown


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
EXPECT = None


def get_token():
    """This functions reads file with token and returns it"""
    with open('token.txt', 'r') as token_file:
        return token_file.read().strip()

    raise Exception("Unable to read token from file token.txt")


def send_document(user, file_path):
    """This function sends specified file to selected user"""
    telegram.User.send_document(user, document=open(file_path, 'rb'))


# Comand handlers
def first_message_handler(update, context):
    """Send a greeting message when /start or /help message is sent"""

    response = ("Hi!\n"
                "I am Renderer Bot.\n"
                "I can help you render your LaTeX or Markdown into PDF.\n"
                "Type /latex or /md (/markdown, if you like) and try it!\n"
                )

    update.message.reply_text(response)


def text_handler(update, context):
    """Handle text messages. Mostly used to receive and process LaTeX/Markdown code"""
    global EXPECT

    # TODO: Add messages if file was incorrect

    if EXPECT == 'latex':
        user = update.message.from_user
        pdf_path = render_latex(update.message.text)

        update.message.reply_text('PDF was generated:')
        send_document(user, pdf_path)
        EXPECT = None

    elif EXPECT == 'markdown':
        user = update.message.from_user
        pdf_path = render_markdown(update.message.text)

        update.message.reply_text('PDF was generated:')
        send_document(user, pdf_path)
        EXPECT = None


def latex_handler(update, context):
    """Handle /latex command"""
    global EXPECT
    update.message.reply_text('Send your LaTeX code')
    EXPECT = 'latex'


def markdown_handler(update, context):
    """Handle /markdown command"""
    global EXPECT
    update.message.reply_text('Send your Markdown code')
    EXPECT = 'markdown'


def error_handler(update, context):
    """Log Errors caused by Updates."""
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Starts the bot"""
    updater = Updater(get_token(), use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", first_message_handler))
    dispatcher.add_handler(CommandHandler("help", first_message_handler))
    dispatcher.add_handler(CommandHandler("latex", latex_handler))
    dispatcher.add_handler(CommandHandler("markdown", markdown_handler))
    dispatcher.add_handler(CommandHandler("md", markdown_handler))

    dispatcher.add_handler(MessageHandler(Filters.text, text_handler))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
