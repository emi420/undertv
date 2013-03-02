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
from subprocess import Popen, PIPE
from data import Data

def get_duration(video):
    regex = re.compile("length (.*)")
    position = json.loads(video['position'])[0]
    file_path = 'content/download/' + str(position) + '/' + video['name'] + ".flv"
    print 'Getting info from video: ' + file_path
    proc = Popen(['omxplayer','-i', file_path], stdin = PIPE, stdout = PIPE, stderr = PIPE)
    output = proc.stdout.read()
    duration = regex.findall(output)[0]
    return duration

def reset_data():
    data = Data()
    videos = map(lambda x: {'id':x[0],'data':x[1]}, data.get("video"))
    for item in videos:
        video = json.loads(item['data'])
        video['time'] = 0
        video['duration'] = int(get_duration(video))
        print 'Updating...'
        data.update(item['id'], json.dumps(video))
        
        
def main():
    reset_data()

if __name__ == '__main__':
    main()
