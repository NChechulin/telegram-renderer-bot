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
    global expect

    # TODO: Add messages if file was incorrect
    # TODO: Add file support

    if expect == 'latex':
        user = update.message.from_user
        pdf_path = latex.render(update.message.text)

        update.message.reply_text('PDF was generated:')
        send_document(user, pdf_path)
        expect = None

    elif expect == 'markdown':
        user = update.message.from_user
        pdf_path = md.render(update.message.text)

        update.message.reply_text('PDF was generated:')
        send_document(user, pdf_path)
        expect = None


def latex_handler(update, context):
    """Handle /latex command"""
    global expect
    update.message.reply_text('Send your LaTeX code')
    expect = 'latex'


def markdown_handler(update, context):
    """Handle /markdown command"""
    global expect
    update.message.reply_text('Send your Markdown code')
    expect = 'markdown'


def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(get_token(), use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", first_message_handler))
    dp.add_handler(CommandHandler("help", first_message_handler))
    dp.add_handler(CommandHandler("latex", latex_handler))
    dp.add_handler(CommandHandler("markdown", markdown_handler))
    dp.add_handler(CommandHandler("md", markdown_handler))

    dp.add_handler(MessageHandler(Filters.text, text_handler))

    dp.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
