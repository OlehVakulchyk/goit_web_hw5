# goit_web_hw5
 home work 5
# Курси валют Приват за останні n днів
poetry shell
py currency.py -h --- HELP
py currency.py n  --- n<11 валюти: USD, EUR
py currency.py n -c CHF CZK GBP PLN --- додаткові валюти(на вибір)

cd websocket
py server.py
відкрити сторінку index.html
exchange --- курс валют Приват сьогодні
exchange n --- за останні n днів(n<11>)
логування виклику "exchange" в файл "exchange.log"