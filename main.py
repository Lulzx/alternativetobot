#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hi! Send to me a software's name to find it's alternatives.')


def help(bot, update):
    update.message.reply_text('Help yourself on your own!')


def show(bot, update):
	post=""
	pltoshow=""
	altshow=""
	tagshow=""
	searched=update.message.text
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
	post+="Titles:"+title[0]
	for x in range(0,len(platforms)):
		pltoshow+="#"+platforms[x]+"\n"
	post+="Platforms :"+"\n"+pltoshow+"\n"
	for y in range(0,len(alternativs)):
		altshow+=alternativs[y]+"\n"
	post+="Alternatives :"+"\n"+altshow+"\n"
	for z in range(0,len(tags)):
		tagshow+="#"+tags[z]+"\n"
	post+="genres:"+"\n"+tagshow
	try:
		post+="Website:"+"\n"+creatorwebsite[0]
	except IndexError:
		print(title[0]+"Not Found !")
	update.message.reply_text(post)


def error(bot, update):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    try:
        token = sys.argv[1]
    except IndexError:
        token = os.environ.get("TOKEN")
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, show))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Ready to rock..!")
    updater.idle()


if __name__ == '__main__':
    main()
