import asyncio
import aiohttp
from aiohttp import web
import os
import sys
from urllib.parse import unquote
from html import unescape

from protocol import *


FILES_FOLDER = os.path.join('.', 'files')
IPS_FILE = os.path.join('.', 'ips.txt')


def save_ip(ip_addr):
  if os.path.exists(IPS_FILE):
    with open(IPS_FILE, 'r') as file:
      for line in file.readlines():
        if line.strip() == ip_addr:
          return False
  with open(IPS_FILE, 'a+') as file:
    file.write(ip_addr + '\n')
  return True

# from https://stackoverflow.com/questions/58454190/python-async-waiting-for-stdin-input-while-doing-other-stuff
async def ainput() -> str:
  return await asyncio.to_thread(sys.stdin.readline)

async def input_loop():
  while True:
    input_string = await ainput()
    await send_instruction(input_string)

async def make_my_life_easier(line, port, instruction):
  async with aiohttp.ClientSession() as session:
    async with session.post('http://{target}:{port}/{location}'.format(target=line, port=port, location=instruction.strip())) as response:
      try:
        await response.read()
      except TimeoutError:
        print('No response from', line.strip())

async def send_instruction(instruction):
  if not os.path.exists(IPS_FILE):
    print('No ips.txt file.')
    return False
  
  tasks = set()
  try:
    async with asyncio.TaskGroup() as tg:
      with open(IPS_FILE, 'r') as file:
        for line in file.readlines():
          task = tg.create_task(make_my_life_easier(line.strip(), CLIENT_PORT, instruction))
          tasks.add(task)
          task.add_done_callback(tasks.discard)
  except* aiohttp.client_exceptions.ClientConnectorError:
    print('Could not send instruction.')
  except* aiohttp.client_exceptions.ServerDisconnectedError:
    print('Server disconnected.')
  
  return True
  

routes = web.RouteTableDef()

@routes.get('/{filename}')
async def getf_handler(request):
  filename = unescape(unquote(request.match_info['filename']))
  path = os.path.join(FILES_FOLDER, filename)
  
  if os.path.exists(path):
    return web.FileResponse(path=path, status=200)
  else:
    return web.Response(status=404)

@routes.post('/NOTIFY/ONLINE')
async def online_handler(request):
  ip_addr = request.remote
  
  if save_ip(ip_addr):
    print('New client online:', ip_addr)
  else:
    print('Client online:', ip_addr)
  
  return web.Response()


app = web.Application()
app.add_routes(routes)


async def main():
  runner  = web.AppRunner(app)
  await runner.setup()
  site = web.TCPSite(runner, 'localhost', SERVER_PORT)
  await site.start()
  
  print('Server running')
  
  input_task = asyncio.create_task(input_loop())
  
  while True:
    await asyncio.sleep(60)

if __name__ == '__main__':
  try:
    asyncio.run(main())
  except (KeyboardInterrupt, EOFError):
    print('Shutting down.')