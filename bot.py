"""Class of bot"""

import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import parsing
from rendering import render_latex, render_markdown

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class Bot():
    """Main class of bot, which encapsulates all of interactions with user"""
    logger = None
    updater = None
    dispatcher = None
    expect = None
    token = None

    def __init__(self, token_file_path: str):
        self.__set_token(token_file_path)
        self.logger = logging.getLogger(__name__)
        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.__set_handlers()

    def start(self):
        """Checks if bot is OK and starts it"""
        if self.__check():
            self.updater.start_polling()
            self.updater.idle()
        else:
            raise Exception(
                "Error: one of necessary variables of Bot was None")

    def __check(self):
        """Checks if all necessary variables are set"""
        to_check = [self.logger, self.updater, self.dispatcher]
        return all([i is not None for i in to_check])

    def __set_handlers(self):
        handlers = [
            CommandHandler("start", self.__first_message_handler),
            CommandHandler("help", self.__first_message_handler),
            CommandHandler("latex", self.__latex_handler),
            CommandHandler("markdown", self.__markdown_handler),
            CommandHandler("md", self.__markdown_handler),
            MessageHandler(Filters.text, self.__text_handler),
            MessageHandler(Filters.document, self.__document_handler)
        ]

        for handler in handlers:
            self.dispatcher.add_handler(handler)

        self.dispatcher.add_error_handler(self.__error_handler)

    def __set_token(self, token_file_path: str):
        """Reads file with bot token and sets token"""
        try:
            with open(token_file_path, 'r') as token_file:
                self.token = token_file.read().strip()
        except FileNotFoundError:
            raise Exception(f"File {token_file_path} does not exist")
        except:
            raise Exception(f"Unable to read token from {token_file_path}")

    def __send_document(self, user, file_path):
        """Sends file to selected user"""
        if file_path is not None:
            telegram.User.send_message(user, text='PDF was generated:')
            telegram.User.send_document(user, document=open(file_path, 'rb'))
        else:
            error_msg = 'Error. Please check if code is correct'
            telegram.User.send_message(user, text=error_msg)

    def __get_document_content(self, file_id):
        """Returns content of file by file_id"""
        received_file = telegram.Bot.getFile(self.updater.bot, file_id)

        return parsing.parse_link(received_file['file_path'])

    # Comand handlers
    def __first_message_handler(self, update, context):
        """Sends a greeting message when /start or /help message is sent"""

        response = ("Hi!\n"
                    "I am Renderer Bot.\n"
                    "I can help you render your LaTeX or Markdown into PDF.\n"
                    "Type /latex or /md (/markdown, if you like) and try it!\n"
                    )

        update.message.reply_text(response)

    def __text_handler(self, update, context):
        """Handle text messages. Mostly used to receive and process LaTeX/Markdown code"""
        try:
            code = parsing.parse_text(update.message.text)
            user = update.message.from_user

            if self.expect == 'latex':
                pdf_path = render_latex(code)

                self.__send_document(user, pdf_path)
                self.expect = None

            elif self.expect == 'markdown':
                pdf_path = render_markdown(code)

                self.__send_document(user, pdf_path)
                self.expect = None
            else:
                error_msg = 'Please specify language before rendering code. Type /help for help'
                update.message.reply_text(error_msg)
        except Exception:
            update.message.reply_text('Error. Could not send file')

    def __latex_handler(self, update, context):
        """Handle /latex command"""
        message = (
            'Send your LaTeX code or '
            'link to raw file, file on github, or a paste on pastebin.org'
        )
        update.message.reply_text(message)
        self.expect = 'latex'

    def __markdown_handler(self, update, context):
        """Handle /markdown command"""
        message = (
            'Send your Markdown code or '
            'link to raw file, file on github, or a paste on pastebin.org'
        )
        update.message.reply_text(message)
        self.expect = 'markdown'

    def __document_handler(self, update, context):
        """Handle sent documents"""
        try:
            file_id = update.message.document.file_id
            code = self.__get_document_content(file_id)
            user = update.message.from_user

            if self.expect == 'latex':
                pdf_path = render_latex(code)

                self.__send_document(user, pdf_path)
                self.expect = None

            elif self.expect == 'markdown':
                pdf_path = render_markdown(code)

                self.__send_document(user, pdf_path)
                self.expect = None
            else:
                error_msg = 'Please specify language before rendering code. Type /help for help'
                update.message.reply_text(error_msg)
        except Exception:
            update.message.reply_text('Error. Could not send file')

    def __error_handler(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"',
                            update, context.error)
