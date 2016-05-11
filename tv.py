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


class TV:

    def __init__(self):
        self.directory = settings['VIDEO_PATH']
        self.playpath = None
        self.waitingvideo = None
        self.video = None
        self.files = []
        for file in os.listdir(self.directory):
            if file.endswith(".mp4"):
                self.files.append(file)

        T = threading.Thread(target=self.positionChecker)
        T.daemon = True                           
        T.start()                                 


    def random(self):
        if self.playpath:
            cmd = 'pkill -9 -f "/usr/bin/omxplayer.bin -s ' + self.playpath + ' -o hdmi"'
            os.system(cmd)
        episode = random.choice(self.files)
        self.playpath = self.directory + episode
        print "Play " + self.playpath
        if self.video:
            self.video.stop()
        if self.waitingvideo:
            self.waitingvideo.stop()
        self.video = OMXPlayer(self.playpath,  '-o hdmi', start_playback=True) 

    def stop(self):
        self.video.stop()
        if self.playpath:
            cmd = 'pkill -9 -f "/usr/bin/omxplayer.bin -s ' + self.playpath + ' -o hdmi"'
            os.system(cmd)


    def positionChecker(self):
        self.waitingvideo = OMXPlayer(settings['VIDEO_WAITING_PATH'], '-o hdmi --loop', start_playback=True) 
        while True:
            if self.video:
                if self.video.finished:
                    self.video = None
                if self.waitingvideo and not self.waitingvideo.paused:
                    self.waitingvideo.stop()
                    self.waitingvideo = None

            else:
                if not self.waitingvideo:
                    self.waitingvideo = OMXPlayer(settings['VIDEO_WAITING_PATH'], '-o hdmi --loop', start_playback=True) 

            sleep(0.05)
