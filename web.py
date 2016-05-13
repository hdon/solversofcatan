#!/usr/bin/env python
import BaseHTTPServer, SocketServer, json, os, catan, mimetypes
from bot import Bot
port = 3000

def initGameAndBots():
  global game, bots
  game = catan.Catan()
  game.randomInit(4)
  bots = map(lambda n: Bot(game, n+1), xrange(4))

initGameAndBots()

class CatanHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(self):
    global game, bots
    if self.path == '/':
      self.path = '/index.html'
    if self.path == '/game.json':

      try:
        game.roll()
        game.activePlayer = game.activePlayer % 4 + 1
        bots[game.activePlayer-1].move()
      except:
        raise
        initGameAndBots()

      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
      self.wfile.write(json.dumps({
        'w': game.w
      , 'h': game.h
      , 'land': game.land
      , 'campSites': game.campSites
      , 'routes': game.routes
      , 'playerResources': game.playerResources
      }))
    else:
      # static files
      path = os.path.normpath(os.getcwd()+'/public'+self.path)
      if not path.startswith(os.getcwd()+'/public/'):
        return self.errorResponse(403, 'Forbidden')
      if not os.path.exists(path):
        return self.errorResponse(404, 'Not Found')
      try: f = open(path)
      except: self.errorResponse(500, 'Internal Server Error')
      self.send_response(200)
      ftype = mimetypes.guess_type(path) or 'application/octet-stream'
      self.send_header('Content-Type', ftype)
      self.end_headers()
      self.wfile.write(f.read())
      f.close()

  def errorResponse(self, code, message):
    self.send_response(code)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    self.wfile.write('<h1>%d</h1><h2>%s</h2>' % (code, str(message)))
      

SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(('', port), CatanHTTPRequestHandler)
print 'serving at port', port
httpd.serve_forever()
