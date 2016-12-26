import os
import sys
import random
import time

import telepot
import yaml


def usage():
    print('bot.py quotes.yml keywords.yml <token>')


if len(sys.argv) != 4:
    usage()
    exit(0)


if not os.path.exists(sys.argv[1]):
    print(sys.argv[1] + ' does not exist')
    exit(0)

if not os.path.exists(sys.argv[2]):
    print(sys.argv[2] + ' does not exist')
    exit(0)


bot = None
try:
    bot = telepot.Bot(sys.argv[3])
except:
    print('Unable to instantiate the bot')
    exit(0)


with open(sys.argv[1]) as file:
    try:
        quotes = yaml.load(file.read())['quotes']
    except:
        print('Unable to read quotes')


with open(sys.argv[1]) as file:
    try:
        keywords = yaml.load(file.read())['keywords']
    except:
        print('Unable to read keywords')


def handle(message):
    if 'text' not in message:
        return

    if not any(keyword in message['text'] for keyword in keywords):
        return

    bot.sendMessage(message['chat']['id'], random.choice(quotes))


bot.message_loop(handle)

while 1:
    time.sleep(10)
