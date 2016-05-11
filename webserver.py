''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    API Server
    
    Create a simple web server.
 
'''

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from tv import TV
import os
from os import curdir, sep

'''
APIServer create a simple web server to control
the TV using HTTP requests
'''
class APIServer(BaseHTTPRequestHandler):

    tv = TV()

    def do_GET(self):
               
        try:
            if self.path == "/":
                self.path = "/index.html"

            if self.path.endswith(".png"):
                mime = "image/png"

            elif self.path.endswith(".jpg"):           
                mime = "image/jpeg"

            else:           
                mime = "text/html"

            self.send_response(200)
            self.send_header("Content-type", mime)
            self.send_header('Allow', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            if self.path == "/random":
                APIServer.tv.random()
            elif self.path.endswith(".png") or self.path.endswith(".jpg") or self.path.endswith(".html"):
                f = open(curdir + sep + self.path, 'r') 
                self.wfile.write(f.read())
                f.close()

            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)        


def main():
  
   try:
        server = HTTPServer(('', 80), APIServer)
        print 'Started Under TV httpserver'
        server.serve_forever()
    
   except KeyboardInterrupt:
        print '^C received, shutting down server'
        os.system('killall omxplayer.bin')
        server.socket.close()

if __name__ == '__main__':
    main()

