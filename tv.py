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
from settings import settings

class TV:

    def __init__(self):
        self.directory = settings['VIDEO_PATH']
    
    def random(self):
        print "Next channel"
        episode = random.choice(os.listdir(self.directory))
        cmd = "nohup omxplayer -b -o hdmi "+"'"+self.directory+episode+"' &"
        os.system('killall omxplayer.bin')
        os.system(cmd)

    def next_ch(self):
        print "Next channel"

    def prev_ch(self):
        print "Prev channel"
            
    def stop(self):
        self.timer.cancel()
                    
