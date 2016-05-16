''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    Web Server
    
    Simple web server.
 
'''

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from tv import TV
from settings import settings
from os import curdir, sep
import os

tv = TV()

'''
APIServer create a simple web server to control
the TV using HTTP requests
'''
class APIServer(BaseHTTPRequestHandler):

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

            if self.path.endswith(".png") or self.path.endswith(".jpg"):
                f = open(curdir + sep + self.path, 'r') 
                self.wfile.write(f.read())
                f.close()
            elif self.path.endswith(".html"):
                f = open(curdir + sep + "index.html", 'r') 
                self.wfile.write(f.read())
                f.close()

            elif self.path == "/random":
                tv.random()
                self.wfile.write("1")

            elif tv.video:
                if self.path == "/stop":
                    tv.stop()
                    self.wfile.write("1")
                elif self.path == "/pause":
                    tv.video.toggle_pause()
                    self.wfile.write("1")
                elif self.path == "/skip_ahead":
                    tv.video.skip_ahead()
                    self.wfile.write("1")
                elif self.path == "/skip_back":
                    self.wfile.write("1")
                    tv.video.skip_back()

            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)        


def main():
  
   try:
        if settings['CONTINUOUS_PLAYBACK']:
            tv.random()
        server = HTTPServer(('', 80), APIServer)
        print 'Started Under TV httpserver on port 80'
        server.serve_forever()
    
   except KeyboardInterrupt:
        print '^C received, shutting down server'
        os.system('killall omxplayer.bin')
        server.socket.close()

if __name__ == '__main__':
    main()

