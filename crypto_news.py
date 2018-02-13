#! /usr/bin/env python

"""
Generate markdown files based on coindesk rss feed and price trigger (change % last hr) on coinmarketcap

"""

__author__ = "merou"

from coinmarketcap import Market
import os
from datetime import datetime
import time
import textwrap
import feedparser
import slugify
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

TRACKING_COINS = ['STRAT','BTC','DASH','EOS','GNO','USDT','ETC','ETH','ICN','LTC','MLN','REP','XDG','XMR','XRP','ZEC']
URL = 'http://feeds.feedburner.com/CoinDesk'
MARKDOWN_DATA = '/tmp/crypto'
PERCENTAGE_CHANGE = 2


def blog_post(coin,percent_change_1h,price_usd):
    ts = time.time()
    timeid = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    title = '{0} went up {1}% last hr(${2})'.format(coin,percent_change_1h,price_usd)
    title_f = unicode(title)
    postid = timeid+'-'+slugify.slugify(title_f)+'.md'
    post = MARKDOWN_DATA+'/'+postid
    contents = textwrap.dedent(
    """\
    ---
    title:  """+title+"""
    date:   """+timestamp+"""
    categories:
    - crypto
    layout: post
    featured_image: "/images/cover.jpg"
    external_url: \"https://coinmarketcap.com/currencies/"""+coin.lower()+"""/\"
    ---
    > ![alternate text](https://files.coinmarketcap.com/static/img/coins/32x32/"""+coin.lower()+""".png) More information on coinmarketcap
    """
    )
    file = open(post,'w')
    file.write(contents)
    file.close()
    print "ADDING: {0}".format(post)


def post_coindesk(title,link,author,published,published_date):
    title = '"{0}"'.format(title)
    postid = published_date+'-'+slugify.slugify(unicode(title))+'.md'
    post = MARKDOWN_DATA+'/'+postid
    contents = textwrap.dedent(
    """\
    ---
    title:  """+title.replace(":","")+"""
    date:   """+published+"""
    categories:
    - crypto
    layout: post
    featured_image: "/images/cover.jpg"
    external_url: \""""+link+"""\"
    ---
    > Posted on coindesk by """+author+"""
    """
    )
    file = open(post,'w')
    file.write(contents)
    file.close()
    print "ADDING: {0}".format(post)


def main():
    coinmarketcap = Market()
    moving_coins = [d for d in coinmarketcap.ticker() if d['symbol'] in TRACKING_COINS and float(d['percent_change_1h']) > PERCENTAGE_CHANGE]
    for el in moving_coins:
      blog_post(el['name'],el['percent_change_1h'],el['price_usd'])

    d = feedparser.parse(URL)
    d.feed.title
    d.feed.link
    d.feed.subtitle

    for l in d['entries']:
      dt = time.strftime('%Y-%m-%d %H:%M:%S', l['published_parsed'])
      dt_date = time.strftime('%Y-%m-%d', l['published_parsed'])
      post_coindesk(l['title'].encode('utf-8').strip(),l['link'],l['author'],dt,dt_date)


if __name__ == '__main__':
   main()

