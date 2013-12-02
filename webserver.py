''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    API Server
    
    Create a simple web server.
 
'''

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from tv import TV

'''
APIServer create a simple web server to control
the TV using HTTP requests
'''
class APIServer(BaseHTTPRequestHandler):

    tv = TV()

    def do_GET(self):

        self._setHeaders() 
               
        path = self.path        
        if path == "/next_ch":
            APIServer.tv.next_ch()

        elif path == "/prev_ch":
            APIServer.tv.prev_ch()

        elif path == "/vol_up":
            APIServer.tv.vol_up()

        elif path == "/vol_down":
            APIServer.tv.vol_down()

        elif path == "/stop":
            APIServer.tv.stop()

        elif path == "/power":
            APIServer.tv.power()
        
        self.wfile.write("1")
           
        return
        
    def _setHeaders(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Allow', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


def main():
  
   try:
        server = HTTPServer(('', 80), APIServer)
        print 'Started Under TV httpserver'
        server.serve_forever()
    
   except KeyboardInterrupt:
        print '^C received, shutting down server'
        APIServer.tv.stop()
        server.socket.close()

if __name__ == '__main__':
    main()

