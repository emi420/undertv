''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    Download random video content
 
'''

import string
import os
import urllib
import random
import json

from command import Run

class ContentDownloader:

   def __init__(self):
        self.keywords = []
        self.random = True
        self.dest = "/home/pi/undertv-server/content/download/"
        self.connector = YouTubeConnector()

   def start(self):
        if self.random:
            print "Start searching ..."
            video_list = self.connector.search(self.keywords)
            if video_list:
                (video_url, video_id) = self.connector.choiceRandom(video_list)
            else:
                self.start()
            if self._videoExists(video_id):
                  # FIXME CHECK
                  self.start()        
            else:
                  print "Downloading video: " + video_url            
                  self.connector._download(video_url, video_id, self.dest)    
                  self.start()
               
   def _videoExists(self, name):
        dest_path = self.dest + name            
        if os.path.exists(dest_path) or \
           os.path.exists(dest_path + ".part") or \
           os.path.exists(dest_path + ".mp4") or \
           os.path.exists(dest_path + ".flv") or \
           os.path.exists(dest_path + ".video") or \
           os.path.exists(dest_path + ".mp4.part") or \
           os.path.exists(dest_path + ".flv.part") or \
           os.path.exists(dest_path + ".video.part"):
           return True
        else:
           return False

class YouTubeConnector:
    def __init__(self):
        self.source = "https://gdata.youtube.com/feeds/api/videos?q=%keywords%&orderby=published&max-results=10&v=2&alt=json"
    
    def search(self, keywords):
        url = self.source.replace('%keywords%',random.choice(keywords))
        print "Downloading result: " + url
        try:
            f = urllib.urlopen(url)        
            result = f.read()
            videos = json.loads(result)
            return videos
        except:
            "Error"
        
    def choiceRandom(self, video_list):
        video = random.choice(video_list['feed']['entry'])
        video_url = video['media$group']['media$player']['url']
        video_id = video['media$group']['yt$videoid']["$t"]
        return (video_url, video_id)
    
    def _download(self, video_url, video_id, dest):
        os.chdir(dest)
        run = Run()
        run.command(['youtube-dl', video_url], shell = False, timeout = 300)
        

def main():
   print "Initializing content downloader..."
   
   cdl = ContentDownloader()
   # Sample keywords
   cdl.keywords = ["rock","danza","expresion","arte","baile","gracioso","divertido","perros","animales","naturaleza","charly garcia","david lynch","cosas locas","mate","animacion","paralell world","cualca","stand up","monologos","aunque usted no lo crea","ciudad","tecnologia"]

   cdl.random = True
   cdl.start()
     
if __name__ == '__main__':
   main()     
