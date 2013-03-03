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
import re
from subprocess import Popen, PIPE
from command import Run
from data import Data
from settings import settings

def get_duration(file_path):
    duration = 0
    try:
        regex = re.compile("length (.*)")
        print 'Getting info from video: ' + file_path
        proc = Popen(['omxplayer','-i', file_path], stdin = PIPE, stdout = PIPE, stderr = PIPE)
        output = proc.stdout.read()
        duration = regex.findall(output)[0]
    except:
        pass
    return duration

class ContentDownloader:

   def __init__(self):
        self.data = Data()
        self.current_content = 0;
        self.current_content_limit = settings['CONTENT_DOWNLOADER_LIMIT'];
        self.current_playlist = 0;
        self.dest = settings['BASE_PATH'] + "content/download/"
        self.playlists = self.data.all("playlist")
        self.connector = YouTubeConnector()

   def start(self):
        print "Start searching ..."
        restart = False

        # Get video index
        video_index = self.current_content
        
        # Get video list from playlist
        try:
            video_yt_id = str(json.loads(self.playlists[self.current_playlist][1])['playlist'])
        except:
            import pdb; pdb.set_trace()
        video_list = self.connector.get(video_yt_id)      
        
        # Get video data from playlist using index
        if video_list:
            (video_url, video_id) = self.connector.choice(video_list, video_index)
        else:
            restart = True
        
        print "Video id: " + video_id
        
        if self._videoExists(video_id) or self._videoExists(video_id + "-watched"):
              print "Video exists"
        else:
              # Destination
              dest = self.dest + str(self.current_playlist) + "/"
              
              print "Downloading video: " + video_url
              print " To:" + dest

              # Make dir
              if not os.path.exists(dest):
                  os.mkdir(dest)

              # Create a process to download video
              self.connector._download(video_url, dest)   
        
              print "Download finished."
     
              video = '{"watched":false'
              video = video + ', "position": "[' + str(self.current_playlist)
              video = video + ',' + str(video_index) + ']"'
              video = video + ', "name": "' + video_id + '"'
              video = video + ', "time": "0"'
            
              duration = get_duration(dest + video_id + '.flv')
              video = video + ', "duration": ' + str(duration) + ' }'
            
              self.data.create("video", video)
                    
        self.current_content = self.current_content + 1

        if self._videoExists(video_id + "-watched"):
            self.current_content_limit = self.current_content_limit + 1
            
        if self.current_content == self.current_content_limit:
               self.current_content = 0
               self.current_content_limit = settings['CONTENT_DOWNLOADER_LIMIT']
               self.current_playlist = self.current_playlist + 1;
               # TODO:
               # If the item is the last one, go back to the first item

        print "Playlist " + str(self.current_playlist) + "/" + str(len(self.playlists))
        if self.current_playlist < len(self.playlists):
            restart = True
        else:
            restart = False
         
        if restart:
            self.start()
               
   def getCurrent(self):
        # FIXME CHECK
        # Get current video from playlist 
        return self.playlists[self.current_playlist][self.current_content]            
               
   def _videoExists(self, name):
        dest_path = self.dest + str(self.current_playlist) + "/" + name            
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
    def _download(self, video_url, dest):
        os.chdir(dest)
        run = Run()
        run.command(['youtube-dl', video_url], shell = False, timeout = -1)
        

def main():
   print "Initializing content downloader..."
   cdl = ContentDownloader()
   cdl.start()
     
if __name__ == '__main__':
   main()     
