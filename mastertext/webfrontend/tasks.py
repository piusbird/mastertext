"""Backround tasks for webapp"""
from datetime import datetime
import gevent
from mastertext.importer import fetch_and_parse
from mastertext.singleton import BorgCache, StoreConnect
from mastertext.utils import MasterTextError
from mastertext.webfrontend import app
from mastertext.models import Error, WordImage
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def import_task(url):
    gevent.idle()

    ts = StoreConnect().get_objstore()

    with app.app_context():
        try:
            text = fetch_and_parse(url)
            ts.create_object(text)
        except MasterTextError as e:
            Error.create(date=datetime.now(), message=str(e))


def flush_cache():
    bc = BorgCache()
    bc.cache = {}
    gevent.spawn_later(1800, flush_cache)


def __wordcloud(text):
    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(text)

    # Convert the WordCloud object to an image
    plt.figure(figsize=(8,8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    
    # Convert the image to HTML
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.read()).decode()
    
    
    return img_base64

def generate_wordimage_single(hashid):
   
    gevent.idle()
    ts = StoreConnect().get_objstore()
    text = None

    with app.app_context():
        try:
            text = ts.retrieve_object(hashid)
        except MasterTextError as e:
            Error.create(date=datetime.now(), message=str(e))
            return
    cloud = __wordcloud(text)
    WordImage.create(phash=hashid, data=cloud)

    

   
