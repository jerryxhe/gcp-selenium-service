#!/usr/bin/env python3
from selenium import webdriver as wd
from pyvirtualdisplay import Display
import sys
os.environ['PATH'] += ':'+os.path.dirname(os.path.realpath(__file__))

js = {
  'evernote_article':{
    'delay':5,
    'js2r':{'html':"""document.body.querySelectorAll('iframe')[0].contentWindow.document.lastChild.outerHTML""",
                   'text':"""document.body.querySelectorAll('iframe')[0].contentWindow.document.lastChild.innerText"""
                  }
  }
}

if __name__="__main__":
  ev_url = sys.argv[1] if len(sys.argv)>=2 else "https://www.evernote.com/shard/s637/sh/d2d5c174-4f11-4ec7-9e39-626371f0471d/d3da04f4dfb15d8c755922f0c16c23f0"
  from time import time
  display = Display(visible=0, size=(1024, 768))
  display.start()
  d = wd.Firefox()
  d.get(ev_url)
  task_spec = js['evernote_article']
  _ans = {}
  start_time =  time()
  for result_name,js_code in task_spec['js2r']:
    try:
      _ans[result_name] = d.execute_script("return " + js_code)
    except Exception as e:
      print(traceback.format_exc())
      print(str(e))
   d.close()
   display.stop()
   end_time = time()
   _ans['seconds_elapsed']= int((end_time-start_time)*1000)
   import json
   print(json.dumps(_ans))
