import redis
from time import sleep

for _ in range(1000):
  sleep(5)
  r = redis.Redis()
  r.publish('ev_url', "https://www.evernote.com/shard/s275/sh/30a0ec22-b7e0-414f-be36-4bdad2ea36fa/387e0a0512d6080f440dcb4d7a86cd5c")
  res = r.get('selenium_result')
  if res is not None:
    print(res)
