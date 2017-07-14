import json
import os
import sys
import random
import time

import telepot
import yaml

try:
    bot = telepot.Bot(os.environ['TELEGRAM_API_KEY'])
except telepot.exception.BadHTTPResponse:
    print('TELEGRAM_API_KEY not set')
    exit(1)


me = bot.getMe()


def usage():
    print('bot.py quotes.yml keywords.yml')


if len(sys.argv) != 3:
    usage()
    exit(0)


if not os.path.exists(sys.argv[1]):
    print(sys.argv[1] + ' does not exist')
    exit(0)

if not os.path.exists(sys.argv[2]):
    print(sys.argv[2] + ' does not exist')
    exit(0)


with open(sys.argv[1]) as file:
    try:
        quotes = yaml.load(file.read())['quotes']
    except:
        print('Unable to read quotes')


with open(sys.argv[2]) as file:
    try:
        keywords = yaml.load(file.read())['keywords']
    except:
        print('Unable to read keywords')


def handle(message):
    message['to'] = me

    with open('/var/log/quote-bot/messages.log', 'a') as file:
        file.write(json.dumps(message) + '\n')

    if 'text' not in message:
        return

    if not any(keyword in message['text'].lower() for keyword in keywords):
        return

    bot.sendMessage(message['chat']['id'], random.choice(quotes))


bot.message_loop(handle)

while 1:
    time.sleep(10)
