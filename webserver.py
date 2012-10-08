''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)

'''

import string
import os, sys
from subprocess import Popen, PIPE
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class Content:

    def __init__(self):
        self.source = "/home/pi/undertv-server/content/download/"
        self.list = []
        self.count = 0
        self.update()
    
    def update(self):
        self.list = os.listdir(self.source)
        self.count = len(self.list)
        
    def get(self, id):
        return self.source + self.list[id]
        
class TV:

    def __init__(self):
        self.current_vol = 40
        self.status = 0
        self.current_ch = 0
        self.content = Content()

    def next_ch(self):
        print "Next channel"
        self.current_ch = self.current_ch + 1
        if self.current_ch == self.content.count:
            self.current_ch = 0
        print "#" + str(self.current_ch)     
        self._play()

    def prev_ch(self):
        print "Prev channel"
        self.current_ch = self.current_ch - 1
        if self.current_ch < 0:
            self.current_ch = self.content.count - 1 
        print "#" + str(self.current_ch)    
        self._play()

    def vol_up(self):
        self.current_vol = self.current_vol + 10
        print "Volume up " +  str(self.current_vol) + "%"
        if self.current_vol > 100:
           self.current_vol = 100
        # Change volume here

    def vol_down(self):
        self.current_vol = self.current_vol - 10
        print "Volume down " +  str(self.current_vol) + "%"
        if self.current_vol < 0:
           self.current_vol = 0
        # Change volume here

    def power(self):
        if self.status == 0:
            print "Power On"
            self.status = 1
            self.content.update()
            self._play()
        else:
            print "Power Off"
            self.status = 0
            self._stop()
        
    def _play(self):
        path = self.content.get(self.current_ch)
        self._stop()
        self._player(path)

    def _stop(self):
        # FIXME CHECK
        os.system('pkill omxplayer')
    
    def _player(self, path):
        print "Play: " + path
        pipe = Popen(['omxplayer', path], stdout = PIPE, stderr = PIPE)
        print 'pid =',pipe.pid

class TVHandler(BaseHTTPRequestHandler):

    tv = TV()

    def do_GET(self):

        self._setHeaders() 
               
        path = self.path        
        if path == "/next_ch":
            TVHandler.tv.next_ch()

        elif path == "/prev_ch":
            TVHandler.tv.prev_ch()

        elif path == "/vol_up":
            TVHandler.tv.vol_up()

        elif path == "/vol_down":
            TVHandler.tv.vol_down()

        elif path == "/stop":
            TVHandler.tv.stop()

        elif path == "/power":
            TVHandler.tv.power()
           
        return
        
    def _setHeaders(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Allow', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

def main():
  
   try:
        server = HTTPServer(('', 80), TVHandler)
        print 'Started Under TV httpserver'
        server.serve_forever()

   except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

