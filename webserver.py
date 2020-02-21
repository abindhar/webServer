"""
A Simple Webserver
Author: Abindu Dhar
"""

from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """If incoming HTTP request is GET
        """
        #full_path = os.getcwd() + self.path
        #if not os.path.exists(full_path):
        #self.path = os.getcwd() + self.path
        if self.path == "/":
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
        except:
            file_to_open = "Error 404: File Not Found!"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open,'utf-8'))

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), RequestHandler)
        print(f"HTTP Server running on port: {port}...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping HTTP Server")
        server.socket.close()
    

if __name__=='__main__':
    main()
