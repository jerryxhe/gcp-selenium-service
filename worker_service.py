import os
import traceback

from flatten_dict import flatten
import spacy
nlp = spacy.load("en_core_web_sm")

from flask import Flask, jsonify, Response
from selenium import webdriver as wd
from selenium.common.exceptions import StaleElementReferenceException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pyvirtualdisplay import Display
import re
from toolz import itertoolz, compose
from toolz.curried import map as cmap, sliding_window, pluck
from sklearn.feature_extraction.text import CountVectorizer

import os
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,Text,String,Float,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

# Base.metadata.bind = cnx
# DBSession = sessionmaker(bind=cnx)

app = Flask(__name__)

# Add the webdrivers to the path
os.environ['PATH'] += ':'+os.path.dirname(os.path.realpath(__file__))+"/bin"

@app.route('/',methods=['GET'])
def index():
    return 'Headless browser service with pubsub'

@app.route('/test/', methods=['GET'])
def get_cnbc_article():
    """downloads the HTML of a CNBC article saved in Evernote"""
    try:
        display = Display(visible=0, size=(1024, 768))
        display.start()
        d = webdriver.Firefox()
        d.get("https://www.evernote.com/shard/s637/sh/d2d5c174-4f11-4ec7-9e39-626371f0471d/d3da04f4dfb15d8c755922f0c16c23f0") 
        find_iframe = By.CSS_SELECTOR, 'iframe.gwt-Frame'
        find_html = By.TAG_NAME, 'html'
        d.close()
        display.stop()
        return jsonify({'success': True, "result": page_source[:500]})
    except Exception as e:
        print traceback.format_exc()
        return jsonify({'success': False, 'msg': str(e)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
