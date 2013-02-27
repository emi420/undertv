''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    Content downloader
 
'''

import string
import os
import urllib
import random
import json

from command import Run
from models import Data

class ContentDownloader:

   def __init__(self):
        self.data = Data()
        self.current_content = 0;
        self.current_playlist = 0;
        self.dest = "/home/pi/undertv-server/content/download/"
        self.playlists = self.data.get("playlist")
        self.connector = YouTubeConnector()

   def start(self):
        print "Start searching ..."
        restart = False

        # Get video index
        video_index = self.current_content
        
        # Get video list from playlist
        video_yt_id = str(json.loads(self.playlists[self.current_playlist][1])['playlist'])
        video_list = self.connector.get(video_yt_id)      
        
        # Get video data from playlist using index
        if video_list:
            (video_url, video_id) = self.connector.choice(video_list, video_index)
        else:
            restart = True
        
        if self._videoExists(video_id):
              # FIXME CHECK
              restart = True
        else:
              # Destination
              dest = self.dest + str(self.current_playlist) + "/"
              
              print "Downloading video: " + video_url
              print " To:" + dest

              # Make dir
              if not os.path.exists(dest):
                  os.mkdir(dest)

              # Create a process to download video
              self.connector._download(video_url, video_id, dest)   
        
        print "Download finished."

        video = '{"watched":false'
        video = video + ', "position": "[' + str(self.current_playlist)
        video = video + ',' + str(video_index) + ']"'
        video = video + ', "name": "' + video_id + '"'
        video = video + ', "time": "0"'
        
        # TODO: get video duration
        video = video + ', "duration": "0"}'
        
        self.data.create("video", video)
                
        self.current_content = self.current_content + 1
        if self.current_content == 2:
               self.current_content = 0
               self.current_playlist = self.current_playlist + 1;
               # FIXME CHECK
               # If the item is the last one, go back to the first item (?)


        if self.current_playlist < len(self.playlists):
            restart = True
         
        if restart:
            self.start()
               
   def getCurrent(self):
        # FIXME CHECK
        # Get current video from playlist 
        return self.playlists[self.current_playlist][self.current_content]            
               
   def _videoExists(self, name):
        dest_path = self.dest + name            
        if os.path.exists(dest_path) or \
           os.path.exists(dest_path + ".mp4") or \
           os.path.exists(dest_path + ".flv") or \
           os.path.exists(dest_path + ".video"):
           return True
        else:
           return False

class YouTubeConnector:
    ''' Check playlists and download videos '''

    def __init__(self):
        self.source = "https://gdata.youtube.com/feeds/api/playlists/%playlistid%?v=2&alt=json"
    
    # Get a playlist
    def get(self, playlist):
        url = self.source.replace('%playlistid%',playlist)
        print "Downloading: " + url
        try:
            f = urllib.urlopen(url)        
            result = f.read()
            videos = json.loads(result)
            return videos
        except:
            "Error"
        
    # Choice a video
    def choice(self, video_list, index):
        video = video_list['feed']['entry'][index]
        video_url = video['media$group']['media$player']['url']
        video_id = video['media$group']['yt$videoid']["$t"]
        return (video_url, video_id)
    
    # Download to local disk
    def _download(self, video_url, video_id, dest):
        os.chdir(dest)
        run = Run()
        run.command(['youtube-dl', video_url], shell = False, timeout = -1)
        

def main():
   print "Initializing content downloader..."
   cdl = ContentDownloader()
   cdl.start()
     
if __name__ == '__main__':
   main()     
