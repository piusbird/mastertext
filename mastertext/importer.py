from bs4 import BeautifulSoup
import urllib.request as urllib2
from mastertext.singleton import StoreConnect
import gevent
import re
DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/86.0"



def fetch_and_parse(url, user_agent=DEFAULT_USER_AGENT):
    req = urllib2.Request(url, data=None, headers={'User-Agent':user_agent})
    html_page = urllib2.urlopen(req)
    soup = BeautifulSoup(html_page, features="lxml")
    text = soup.find_all(text=True)
    output = ''
    blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head', 
    'input',
    'script',
    'style',
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return output

def import_task(url):
    gevent.idle()
    ts = StoreConnect().get_objstore()
    text = fetch_and_parse(url)
    ts.create_object(text)