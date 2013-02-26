''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    Remote TV controller
 
'''

import string
import os, sys, signal
import json
from time import time
from contentdl import ContentDownloader
from subprocess import Popen, PIPE
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from models import Data

class Content:

    def __init__(self):
        self.data = Data()
        self.playlists = map(lambda x: {'id':x[0],'data':x[1]}, self.data.get("playlist"))
        self.count = len(self.playlists)
        self.list = []
        self.source = "/home/pi/undertv-server/content/download/"
    
    def update(self):
        self.list = map(lambda x: {'id':x[0],'data':x[1]}, self.data.get("video"))

    def getByPosition(self, position):
        pos = str(position).replace(' ','')
        return filter((lambda x: json.loads(x['data'])["position"] == pos), self.list)[0]

class TV:

    def __init__(self):
        self.current_vol = 40
        self.status = 0
        self.startTime = time()
        self.downloadPID = 0
        self.proc = None
        self.current = [0,0]
        self.content = Content()
    
    def _sendCommand(self, cmd):
        try:
            self.proc.communicate(cmd)
        except:
            pass

    def next_ch(self):
        print "Next channel"
        self.current = [self.current[0]+1,self.current[1]] 
        if self.current[0] == self.content.count:
            self.current[0] = 0
        self.content.update()
        print "#" + str(self.current)     
        self._play()

    def prev_ch(self):
        print "Prev channel"
        self.current = [self.current[0]-1,self.current[1]] 
        if self.current[0] < 0:
            self.current[0] = self.content.count
        self.content.update()
        print "#" + str(self.current)    
        self._play()

    def vol_up(self):
        self.current_vol = self.current_vol + 10
        print "Volume up " +  str(self.current_vol) + "%"
        if self.current_vol > 200:
           self.current_vol = 200
        #self._sendCommand('+')

    def vol_down(self):
        self.current_vol = self.current_vol - 10
        print "Volume down " +  str(self.current_vol) + "%"
        if self.current_vol < -100:
           self.current_vol = -100
        #self._sendCommand('-')

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
        self.video = self.content.getByPosition(self.current)
        self._stop()
        self.startTime = time()
        self._player( json.loads(self.video['data'])['name'], self.content.source)

    def _stop(self):
        self.time = int(time() - self.startTime)
        print "Stopped at " + str(self.time) + " s"
        video = json.loads(self.video['data'])
        video['time'] = self.time
        self.content.data.update(self.video['id'], json.dumps(video))
        self._sendCommand("q")
        if self.downloadPID > 0:
            try:
                os.kill(self.downloadPID, signal.SIGKILL)
            except:
                pass
    
    def _player(self, path, source):
        file_path = source + str(self.current[0]) + "/" + path
        print "Play: " + file_path
        if file_path.find(".part") > -1:
            os.chdir(source)
            video_id = path.replace(".part","").replace(".mp4","").replace(".flv","").replace(".video","")
            print "File " + file_path + " exists, downloading ... (videoid=" + video_id + ")"
            self.downloadPID = self._fullDownload(video_id)
        
        ''' Add -r option to omxplayer if you want fullscreen mode '''
        try:
            time = str(json.loads(self.video['data'])['time'])
            self.proc = Popen(['omxplayer', '-3','-w','-l ' + time, file_path], stdin = PIPE, stdout = PIPE, stderr = PIPE)
        except:
            pass

    def _fullDownload(self, video_id):
        p = Popen(['youtube-dl', "http://youtube.com/watch?v=" + video_id])
        return p.pid


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
        
        self.wfile.write("1")
           
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

