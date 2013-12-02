''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    TV
 
    TV video playing and controls and Content read and update 
 
'''

import string
import os, sys, signal
import json
import time
from subprocess import Popen, PIPE
from data import Data
from threading import Timer

class Content:

    def __init__(self):
        
        # Initialize data connection
        self.data = Data()
        
        # Initialize video list
        self.list = []
        
        # Read video list
        self.list = map(lambda x: {'id':x[0],'data':x[1]}, self.data.all("video"))
        
        # Video count
        self.count = len(self.list)
        
        
class TV:

    def __init__(self):
        self.current_vol = 40
        self.status = 0
        self.startTime = time.time()
        self.downloadPID = 0
        self.proc = None
        self.timer = None
        self.current = 0
        self.content = Content()
        self.list = self.content.list
        self.video = self.list[self.current]
    
    # Send command to omxplayer process
    def _sendCommand(self, cmd):
        try:
            self.proc.communicate(cmd)
        except:
            pass

    def next_ch(self):
        self._stop()
        print "Next channel"
        self.current = self.current + 1
        if self.current == self.content.count:
            self.current = 0
        self._play()

    def prev_ch(self):
        self._stop()
        print "Prev channel"
        self.current = self.current - 1
        if self.current < 0:
            self.current = self.content.count
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
            self._play()
        else:
            print "Power Off"
            self.status = 0
            self._stop()
            
    def stop(self):
        self.timer.cancel()
                    
    def _play(self):
    	
	
	'''try:'''
        self.video = self.list[self.current]
        self.startTime = time.time()
        self._player(json.loads(self.video['data'])['path'])
        '''except:
            self.current = 0
            self.next_ch()
       '''

    def _stop(self):
    
        if self.timer:
            self.timer.cancel()
        
        self.time = int(time.time() - self.startTime)
        print "Stopped at " + str(self.time)

        video = json.loads(self.video['data'])
        try:
            videoTime
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
        self.content.data.update(self.video['id'], json.dumps(video))
        self.current[1] = self.current[1] + 1
        self._play()
    
    def _player(self, file_path):
    
        video = json.loads(self.video['data'])

        print 'Video watched: ' + str(video['watched'])

        if video['watched'] == False:

            print "Play: " + file_path
                
            videoTime = video['time']
            duration = time.strptime(video['duration'], "%H:%M:%S")
            
            remaining = (duration.tm_hour * 3600 + duration.tm_min * 60 + duration.tm_sec) - int(videoTime)
            
            self.timer = Timer(remaining, self._watched)
            self.timer.start()
            
            print "Last stopped at " + str(videoTime)
            print "Remaining time " + str(remaining)
            print "Playing " + file_path + " ..."
            
            self.proc = Popen(['omxplayer','-l ' + str(videoTime), file_path], stdin = PIPE, stdout = PIPE, stderr = PIPE)
            '''self.proc = Popen(['omxplayer ', file_path], stdin = PIPE, stdout = PIPE, stderr = PIPE)'''
            
        else:            
            self.current[1] = self.current[1] + 1
            print "This video was watched, play next";
            self._play()

