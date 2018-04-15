#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
simple telegram bot to send pics dumps by - e.g, fswebcam 
create bot with BotFather, add your token
"""

import telepot
import time

TOKEN='xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    command = msg['text']
    hide_keyboard={'hide_keyboard':True}

    if command == '/camera':
        bot.sendPhoto(chat_id,open('/tmp/photo.jpg', 'rb'),caption=' ',reply_markup=hide_keyboard)

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print 'waiting ...'

while 1:
  time.sleep(10)
