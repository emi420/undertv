''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    Sample data (playlists)
     
'''

from models import Data

def create_sample_data():
    data = Data()
    playlists = [
        'PL3LlaCr57zIGUIsgQ6EabxqI4IyRE1Sn0',
        'PL2D29D1904003925D',
        'PL364EB8D14F2D0E48',
        'PLA7AED6DD71FC3AC2',
    ]
    index = 0
    for playlist in playlists:
        data.create("playlist", '{"playlist": "' + playlist + '", "index":' + str(index) + '}')
        index = index + 1
        
def main():
   print "Creating sample data..."
   create_sample_data()
     
if __name__ == '__main__':
   main()     
