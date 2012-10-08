''' 
    Under TV: Content Downloader 
    
    Copyright 2012 by Emilio Mariscal

'''

import string
import os, sys, signal
import urllib
import random
import json
import shutil

from subprocess import Popen
from subprocess import PIPE

class ContentDownloader:

   def random(self):
        keywords = ["cualca","todo por 2 pesos","cha cha cha","paralell world","capusotto","documental","improcrash","stand up","vorterix","corto","whos line is it anyway subtitulado"]
        f = urllib.urlopen("https://gdata.youtube.com/feeds/api/videos?q=" + random.choice(keywords) + "&orderby=published&max-results=10&v=2&alt=json")
        
        result = f.read()
        videos = json.loads(result)
        path = random.choice(videos['feed']['entry'])['media$group']['media$player']['url']
        videoid = videos['feed']['entry'][0]['media$group']['yt$videoid']["$t"]
        print "Downloading: " + path
        base = "/home/pi/undertv-server/content/download/"

        if os.path.exists(base + videoid):
           self.random()
        elif os.path.exists(base + videoid + ".mp4"):
           self.random()
        elif os.path.exists(base + videoid + ".flv"):
           self.random()        
        else:
           os.chdir(base)
           pipe = Popen(['youtube-dl', path], stdout = PIPE, stderr = PIPE)
           pipe.wait()
           print "Download OK"

           self.random()
      
def main():
   print "Initializing content downloader..."
   cdl = ContentDownloader()
   try:
       cdl.random()
   except:
       cdl.random()
     
if __name__ == '__main__':
   main()     
