import os
import traceback

from flatten_dict import flatten
from flask import Flask, jsonify, Response
from selenium import webdriver as wd
from selenium.common.exceptions import StaleElementReferenceException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

from pyvirtualdisplay import Display
import re
from toolz import itertoolz, compose
from toolz.curried import map as cmap, sliding_window, pluck

import os
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,Text,String,Float,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import subprocess

Base = declarative_base()
# Base.metadata.bind = cnx
# DBSession = sessionmaker(bind=cnx)
app = Flask(__name__)
# Add the webdrivers to the path
os.environ['PATH'] += ':'+os.path.dirname(os.path.realpath(__file__))+"/bin"

js = {
  'evernote_article':{
    'delay':5,
    'js2r':{'html':"""document.body.querySelectorAll('iframe')[0].contentWindow.document.lastChild.outerHTML""",
                   'text':"""document.body.querySelectorAll('iframe')[0].contentWindow.document.lastChild.innerText"""
                  }
  }
}

@app.route('/',methods=['GET'])
def index():
    import redis
    r = redis.Redis(host='localhost')
    try:
        res = r.get('selenium_result')
        return res['html']
    except:
        return 'Headless browser service with background tasks and pubsub'

def background_scraping_task1(ev_url, _task_spec = js['evernote_article']):
    from selenium import webdriver as wd
    from os import sleep
    from pyvirtualdisplay import Display
    import logging,json
    from time import time
    display = Display(visible=0, size=(1024, 768))
    display.start()
    d = wd.Firefox()
    d.get(ev_url)
    sleep(_task_spec['delay'])
    _ans = {}
    start_time =  time()
    for result_name,js_code in _task_spec['js2r']:
        try:
            _ans[result_name] = d.execute_script("return " + js_code)
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error(str(e))
    # cleanup selenium
    d.close()
    display.stop()
    end_time = time()
    _ans['seconds_elapsed']= int((end_time-start_time)*1000)
    # publish the result
    logging.info("result for url {}\n\n".format(ev_url) + json.dumps(_ans))
    
@app.route('/fetch_html', methods=['POST'])
def get_ev_html():
    params = request.get_json()
    ev_url = params['url'] if 'url' in params else "https://www.evernote.com/shard/s637/sh/d2d5c174-4f11-4ec7-9e39-626371f0471d/d3da04f4dfb15d8c755922f0c16c23f0"
    deferred.defer(background_scraping_task1, ev_url)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
