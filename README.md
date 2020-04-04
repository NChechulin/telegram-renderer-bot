## :ru: Русская версия
Версия на русском языке доступна [здесь](README-RU.md)

# Telegram Renderer Bot

This project is a small Telegram bot made for rendering your LaTeX or Markdown code in PDF.
It can be used, if you need to do it on the go, for example, on your smartphone or your friend's computer.

## Uploading methods

Main focus of the project is to give you flexebility in uploading code.
You can upload your code by sending:
* code as a message
* a file
* a link to a file on the Internet
* a link to a file on GitHub
* a link to paste on [Pastebin](http://pastebin.org)

## Setup

Firstly, you have to clone the repo:
```
git clone https://github.com/NChechulin/telegram-renderer-bot.git
cd telegram-renderer-bot
```

Now you need to ensure that `pdflatex` and `python3` are installed on your system.
If everything is OK, install the Python requirements:
```
pip install -r requirements.txt
```

When requirements are installed, register your bot at `@botfather` in Telegram and replace the first line of `token.txt` with your bot's token.

Now we can run the bot:
```
python3 main.py
```

### Solving issues with connection

Telegram might be blocked in Russia, so sometimes bot can't connect to Telegram servers.
To solve this issue you can use VPN (for example, [Windscribe](https://windscribe.com))

