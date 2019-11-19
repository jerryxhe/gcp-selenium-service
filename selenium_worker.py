#!/usr/bin/env python3
import redis
from threading import Thread
from selenium import webdriver as wd
from pyvirtualdisplay import Display
import sys,os,json
import traceback
from time import sleep

os.environ['PATH'] += ':'+os.path.dirname(os.path.realpath(__file__))

js = {
  'evernote_article':{
    'delay':5,
    'js2r':{'html':"""document.body.querySelectorAll('iframe')[0].contentWindow.document.lastChild.outerHTML""",
                   'text':"""document.body.querySelectorAll('iframe')[0].contentWindow.document.lastChild.innerText"""
                  }
  }
}

import threading as t
import subprocess
class BgLowestPriority(t.Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)

    def run(self):
        p = subprocess.Popen('rsync -av /etc/passwd /tmp'.split(),
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, creationflags = subprocess.IDLE_PRIORITY_CLASS)
        self.stdout, self.stderr = p.communicate()

from time import time
class SeleniumChromeWorker(Thread):
    def __init__(self, redis_handle):
        Thread.__init__(self)
        self.redis = redis_handle
        self.pubsub = redis_handle.pubsub()
        self.pubsub.subscribe(['ev_url'])
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.browser = wd.Chrome()
        self.task_spec = js['evernote_article']
    def run(self):
        for ev_url in self.pubsub.listen():
          if 'data' not in ev_url:
            continue
          if isinstance(ev_url['data'], int):
            continue
          print(ev_url['data'])
          self.browser.get(ev_url['data'].decode('ascii'))
          sleep(4)
          _ans = {}  
          start_time =  time()
          for result_name,js_code in self.task_spec['js2r'].items():
            try:
              _ans[result_name] = self.browser.execute_script("return " + js_code).decode('ascii')
            except Exception as e:
              print(traceback.format_exc())
              print(str(e))
          _ans['url'] = ev_url
          end_time = time()
          _ans['seconds_elapsed']= int((end_time-start_time)*1000)
          final_result = json.dumps(_ans)
          self.redis.set('selenium_result', final_result)
          self.redis.publish('ev_result', final_result)

if __name__=="__main__":
    r = redis.Redis('127.0.0.1', port=6379)
    client = SeleniumChromeWorker(r)
    client.start()
