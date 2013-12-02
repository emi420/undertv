''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    Reset data
 
'''

import json
import re
import os
import sys
from subprocess import Popen, PIPE
from data import Data
from settings import settings

rootdir = sys.argv[1]

def get_duration(file_path):
    regex = re.compile("Duration: (.*),")
    ouput = ""
    print 'Getting info from video: ' + file_path
    proc = Popen(["omxplayer -i '" + file_path + "'"], shell = True, stdin = PIPE, stdout = PIPE, stderr = PIPE)
    out = proc.communicate()
    try:
        duration = regex.findall(out[1])[0][0:8]
    except:
        print "(Fail: getting duration)"
        duration = "00:00:00"
    print 'Duration: ' + duration
    return duration 

def create_data():
    data = Data()

    for root, subFolders, files in os.walk(rootdir):
        for filename in files:
            filePath = os.path.join(root, filename)
            print filePath
            video = {}
            video['path'] = filePath
            video['watched'] = 0
 	    video['time'] = "0"
            video['duration'] = get_duration(filePath)
            print 'Updating...'
            data.create('video', json.dumps(video))
        
        
def main():
    create_data()

if __name__ == '__main__':
    main()
