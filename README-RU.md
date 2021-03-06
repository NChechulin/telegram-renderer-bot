## :us: English version
English version is available [here](README.md)

# Telegram Renderer Bot

Этот проект - небольшой Telegram бот, созданный для рендеринга ваших Latex и Markdown документов в PDF.
Он может использоваться, если вам нужно сделать это на ходу, например, со своего смартфона или компьютера товарища.

## Методы загрузки кода

Основной целью прокета была гибкость загрузки кода.
Вы можете сделать это, отправив:
* Код как сообщение
* Файл
* Ссылку на файл в Интернете
* Ссылку на файл на GitHub
* Ссылку на пасту с [Pastebin](http://pastebin.org)

## Установка

Для начала, вам нужно склонировать репозиторий:
```
git clone https://github.com/NChechulin/telegram-renderer-bot.git
cd telegram-renderer-bot
```

Теперь вам нужно убедиться, что программы `pdflatex`, `wkhtmltopdf` и `python3` установлены на вашей системе.
Если все установлено, можно установить зависимости Python:
```
pip install -r requirements.txt
```

Когда зависимости установлены, зарегистрируйте своего бота у `@botfather` в Telegram и замените первую строку файла `token.txt` на токен бота.

Теперь можно запустить бота:
```
python3 main.py
```

