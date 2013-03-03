''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    TV
 
'''

import string
import os, sys, signal
import json
from time import time
from contentdl import ContentDownloader
from subprocess import Popen, PIPE
from data import Data
from threading import Timer

class Content:

    def __init__(self):
        self.data = Data()
        self.playlists = map(lambda x: {'id':x[0],'data':x[1]}, self.data.all("playlist"))
        self.count = len(self.playlists)
        self.list = []
        self.source = "content/download/"
    
    def update(self):
        self.list = map(lambda x: {'id':x[0],'data':x[1]}, self.data.all("video"))

    def getByPosition(self, position):
        pos = str(position).replace(' ','')
        print "Reading info of video " + pos
        return filter((lambda x: json.loads(x['data'])["position"] == pos), self.list)[0]

class TV:

    def __init__(self):
        self.current_vol = 40
        self.status = 0
        self.startTime = time()
        self.downloadPID = 0
        self.proc = None
        self.timer = None
        self.current = [0,0]
        self.content = Content()
    
    def _sendCommand(self, cmd):
        try:
            self.proc.communicate(cmd)
        except:
            pass

    def next_ch(self):
        self._stop()
        print "Next channel"
        self.current = [self.current[0]+1,self.current[1]] 
        if self.current[0] == self.content.count:
            self.current[0] = 0
        self.content.update()
        self._play()

    def prev_ch(self):
        self._stop()
        print "Prev channel"
        self.current = [self.current[0]-1,self.current[1]] 
        if self.current[0] < 0:
            self.current[0] = self.content.count
        self.content.update()
        self._play()

    def vol_up(self):
        self.current_vol = self.current_vol + 10
        print "Volume up " +  str(self.current_vol) + "%"
        if self.current_vol > 200:
           self.current_vol = 200
        # FIXME CHECK
        self._sendCommand('+')

    def vol_down(self):
        self.current_vol = self.current_vol - 10
        print "Volume down " +  str(self.current_vol) + "%"
        if self.current_vol < -100:
           self.current_vol = -100
        # FIXME CHECK
        self._sendCommand('-')

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
            
    def stop(self):
        self.timer.cancel()
                    
    def _play(self):
	try:
            self.video = self.content.getByPosition(self.current)
            self.startTime = time()
            self._player( json.loads(self.video['data'])['name'], self.content.source)
        except:
            self.current[1] = 0
            self.next_ch()

    def _stop(self):
    
        if self.timer:
            self.timer.cancel()
        
        self.time = int(time() - self.startTime)
        video = json.loads(self.video['data'])
        try:
            videoTime = int(video['time'])
        except:
            videoTime = 0
        video['time'] = videoTime + self.time 
        self.content.data.update(self.video['id'], json.dumps(video))
        self._sendCommand("q")
        if self.downloadPID > 0:
            try:
                os.kill(self.downloadPID, signal.SIGKILL)
            except:
                pass
                
    def _watched(self):
        print "Watched!"
        video = json.loads(self.video['data'])
        video['watched'] = True
        
        file_path = self.content.source + str(self.current[0]) + "/" + video['name'] + ".flv"
        renamed_file_path = self.content.source + str(self.current[0]) + "/" + video['name'] + "-watched.flv"
        if os.path.exists(file_path):
            os.rename(file_path, renamed_file_path)
            # TODO: run ContentDownloader as a background process
            # cdl = ContentDownloader()
            # cdl.start(background=true)
        
        # FIXME CHECK: delete original file and create a empty renamed file
        # os.remove(file_path)
        # f = open(renamed_file_path, 'w')
        # f.write('')
        # f.close()
        
        self.content.data.update(self.video['id'], json.dumps(video))
        self.current[1] = self.current[1] + 1
        self._play()
    
    def _player(self, path, source):
    
        video = json.loads(self.video['data'])
        
        print 'Video name: ' + video['name']
        print 'Video watched: ' + str(video['watched'])

        if video['watched'] == False:

            file_path = source + str(self.current[0]) + "/" + path + ".flv"
            print "Play: " + file_path
                
            time = video['time']
            duration = video['duration']
            remaining = int(duration) - int(time)
            
            self.timer = Timer(remaining, self._watched)
            self.timer.start()
            
            print "Last stopped at " + str(time)
            print "Remaining time " + str(remaining)
            print "Playing ..."
            
            self.proc = Popen(['omxplayer','-l ' + str(time), file_path], stdin = PIPE, stdout = PIPE, stderr = PIPE)
            
        else:            
            self.current[1] = self.current[1] + 1
            print "This video was watched, play next, #" + str(self.current);
            self._play()

