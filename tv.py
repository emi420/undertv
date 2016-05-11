''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    TV
 
    TV video playing and controls and Content read and update 
 
'''

import os
import random
from settings import settings
from pyomxplayer import OMXPlayer
from time import sleep
import threading

def positionChecker(video, waitingvideo):
    while True:
        sleep(0.05)
        if video and video.finished and not waitingvideo:
            waitingvideo = OMXPlayer(settings['VIDEO_WAITING_PATH'], '-o hdmi --loop', start_playback=True) 


class TV:

    def __init__(self):
        self.directory = settings['VIDEO_PATH']
        self.playpath = None
        self.waitingvideo = None
        self.video = None
        self.files = []
        self.positionChecker_Thread = None
        for file in os.listdir(self.directory):
            if file.endswith(".mp4"):
                self.files.append(file)

        self.positionChecker_Thread = threading.Thread(target=positionChecker, args=(self.video,self.waitingvideo))
        self.positionChecker_Thread.daemon = True                           
        self.positionChecker_Thread.start()                                 


    def random(self):
        if self.playpath:
            cmd = 'pkill -9 -f "/usr/bin/omxplayer.bin -s ' + self.playpath + ' -o hdmi"'
            os.system(cmd)
        episode = random.choice(self.files)
        self.playpath = self.directory + episode
        print "Play " + self.playpath
        if self.waitingvideo:
            self.waitingvideo.stop()
            self.waitingvideo = None
        self.video = OMXPlayer(self.playpath,  '-o hdmi', start_playback=True) 



