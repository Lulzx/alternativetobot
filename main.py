#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
from lxml import html
import apiai
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi!')


def textMessage(update, context):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer xyzpqrabclol',
    }

    data = '{"queryInput":{"text":{"text":"' + update.message.text + '","languageCode":"en"}},"queryParams":{"timeZone":"Asia/Kolkata"}}'

    response = requests.post('https://dialogflow.googleapis.com/v2/projects/lulzx-4dd1d/agent/sessions/bfc25685-ba30-f876-a361-d0eb9167ce45:detectIntent', headers=headers, data=data)
    response = response.json()
    response = response['queryResult']['parameters']['q']
    response = fetch(response)
    update.message.reply_text(response)


def fetch(query):
    post=""
    pltoshow=""
    altshow=""
    tagshow=""
    searched=query
    urlsearched="http://alternativeto.net/browse/search/?q="+searched+"&ignoreExactMatch=true"
    searchedpage = requests.get(urlsearched)
    searchedtree = html.fromstring(searchedpage.content)
    searchedlink=searchedtree.xpath('//a[@data-link-action="Search"]/@href')
    url="http://alternativeto.net"+searchedlink[0]
    page = requests.get(url)
    tree = html.fromstring(page.content)
    title=tree.xpath('//h1[@itemprop="name"]/text()')
    tags=tree.xpath('//span[@class="label label-default"]/text()')
    platforms=tree.xpath('//li[@class="label label-default "]/text()')
    #image=tree.xpath('//div[@class="image-wrapper"]/img[@src]')
    alternativs=tree.xpath('//a[@data-link-action="Alternatives"]/text()')
    creatorwebsite=tree.xpath('//a[@class="ga_outgoing"]/@href')
    try:
        post+="{}[{}]\n".format(title[0], creatorwebsite[0])+"\n"
    except IndexError:
        post+=title[0]
    for x in range(0,len(platforms)):
        if x is len(platforms)-1:
            pltoshow+="└ "+platforms[x]+"\n"
        else:
            pltoshow+="├ "+platforms[x]+"\n"
    post+="Platforms: "+"\n"+pltoshow+"\n"
    for y in range(0,len(alternativs)):
        if y is len(alternativs)-1:
            altshow+="└ "+alternativs[y]+"\n"
        else:
            altshow+="├ "+alternativs[y]+"\n"
    post+="Alternatives: "+"\n"+altshow+"\n"
    for z in range(0,len(tags)):
	tagshow+="#"+tags[z]+"\n"
    post+="genres:"+"\n"+tagshow
    return post


def help(update, context):
    update.message.reply_text('Help me instead, uhh!')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    try:
        TOKEN = sys.argv[1]
    except IndexError:
        TOKEN = os.environ.get("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, textMessage))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Ready to rock..!")
    updater.idle()


if __name__ == '__main__':
    main()
