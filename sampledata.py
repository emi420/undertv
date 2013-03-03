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
        'PL76D88CE4BF24800A', # Documentales de animales
        'PL1310CCF5883538BF', # Cualca
        'PL2D777F643C59AE11', # Beatles subtitulados
        'PLMbKYkVUcdwRUXovGNkxWQTAziX83OXmM', # Capusotto
        'PLTin6wRbwSbXOMojW8WJ4_bswIE64bV38', # FAIL compilation 2013
        'PL2D29D1904003925D', # Paralell World
        'PL11BB46182D559160', # Escenas de los simpsons
        'PL364EB8D14F2D0E48', # Who's line is it anyway
        'PL5844E4B6DEC2B6EC', # Seinfeld
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
