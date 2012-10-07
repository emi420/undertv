''' 
    Under TV 
    
    Copyright 2012 by Emilio Mariscal

'''

import string
import os, sys, signal
from subprocess import Popen
from subprocess import PIPE
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class TV:

    def __init__(self):
        self.current_ch = 1
        self.pipe = None

    def next_ch(self):
        print "Next channel"
        self.current_ch = self.current_ch + 1
        if self.current_ch == 4:
            self.current_ch = 1
        self.stop()
        self._play()

    def prev_ch(self):
        print "Prev channel"
        self.current_ch = self.current_ch - 1
        if self.current_ch == 0:
            self.current_ch = 3
        self.stop()
        self._play()

    def vol_up(self):
        print "Volume up"

    def vol_down(self):
        print "Volume down"
        
    def stop(self):
        print "Stop"
        print self.pipe
        print 'pid =',self.pipe.pid
        pid = self.pipe.pid
        os.system('pkill omxplayer')
        return
    
    def _play(self):
        path = '/home/pi/under-tv/0' + str(self.current_ch) + '/01.mp4'
        self.pipe = Popen(['omxplayer', path], stdout = PIPE, stderr = PIPE)
        print 'pid =',self.pipe.pid
        return

    def power(self):
        print "Power TV"
        self._play()

class TVHandler(BaseHTTPRequestHandler):

    tv = TV()

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Allow', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        path = self.path
        
        if path == "/next_ch":
            self.wfile.write("Next channel");
            TVHandler.tv.next_ch()
        elif path == "/prev_ch":
            self.wfile.write("Prev channel");
            TVHandler.tv.prev_ch()
        elif path == "/vol_up":
            self.wfile.write("Volume up");
            TVHandler.tv.vol_up()
        elif path == "/vol_down":
            self.wfile.write("Volume down");
            TVHandler.tv.vol_down()
        elif path == "/stop":
            self.wfile.write("Stop");
            TVHandler.tv.stop()
        elif path == "/power":
            self.wfile.write("Power");
            TVHandler.tv.power()
            
        return

def main():
    try:
        server = HTTPServer(('', 80), TVHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

