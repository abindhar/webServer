"""
A Simple Webserver that serves files from the local directory and subdirectories
Author: Abindu Dhar
"""
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
import os, time, json, argparse
import threading

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handles HTTP GET Requests from Client
        """
        path = os.getcwd()+self.path
        if os.path.isdir(path):
            self.list_directory(path)
            return None
        elif os.path.isfile(path):
            try:
                with open(path, 'r', errors='ignore') as f:
                    file_content = f.read()
                self.send_response(200)
            except IOError:
                file_content = "Error 404: File Not Found!"
                self.send_response(404)
        else:
            file_content = "Error 404: Not Found!"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_content,'utf-8'))
        return

    def _get_file_type(self, path):
        """Check if given relative path has a file or directory
        """
        if os.path.isfile(path):
            return 'file'
        if os.path.isdir(path):
            return 'dir'
        return 'unknown'

    def list_directory(self, path):
        try:
            dir_content = os.listdir(path)
        except OSError:
            self.send_response(403)
            self.send_error(HTTPStatus.NOT_FOUND, "Could not list directory")
            return None

        ret = {x: self._get_file_type(os.path.join(path, x))
               for x in dir_content}

        encoded = json.dumps(ret, sort_keys=True).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-type", "text/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

class ThreadedHTTPServer(HTTPServer):
    """Spawn a new thread for each new request
    """
    # Mark threads as non daemonic, for graceful exit
    daemon_threads = False
    block_on_close = True
    _threads = None

    def process_request_thread(self, request, client_address):
        """Runs in a thread and calls Base Class Methods for request processing
        """
        try:
            self.finish_request(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)

    def process_request(self, request, client_address):
        """Start a new thread to process the request
        """
        t = threading.Thread(target = self.process_request_thread,
                             args = (request, client_address))
        t.daemon = self.daemon_threads
        if not t.daemon and self.block_on_close:
            if self._threads is None:
                self._threads = []
            self._threads.append(t)
        t.start()

    def server_close(self):
        """Close and wait for all threads
        """
        super().server_close()
        if self.block_on_close:
            threads = self._threads
            self._threads = None
            if threads:
                for thread in threads:
                    thread.join()


def main():
    parser = argparse.ArgumentParser(prog='webserver.py')
    parser.add_argument('--port', type=int, default=8080, help="The port to listen on")
    args = parser.parse_args()
    port = args.port
    try:
        server = ThreadedHTTPServer(('', port), RequestHandler)
        print(f"Starting HTTP Server, running on port: {port}. Use CTRL+C to stop...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping HTTP Server...")
        server.socket.close()

if __name__=='__main__':
    main()
