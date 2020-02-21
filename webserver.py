"""
A Simple Webserver that serves files from the local directory and subdirectories
Author: Abindu Dhar
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import os, time
import threading

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handles HTTP GET Requests from Client
        """
        thread_name =  threading.currentThread().getName()
        print(f"In Thread: {thread_name}")
        if self.path.endswith("/"):
            file_to_open = "Error 403: Directory Access is Forbidden, specify a file to fetch"
            self.send_response(403)
        else:
            try:
                with open(self.path[1:]) as f:
                    file_to_open = f.read()
                self.send_response(200)
            except IOError:
                file_to_open = "Error 404: File Not Found!"
                self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open,'utf-8'))
        return

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
    try:
        port = 8080
        server = ThreadedHTTPServer(('', port), RequestHandler)
        print(f"Starting HTTP Server, running on port: {port}. Use CTRL+C to stop...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping HTTP Server...")
        server.socket.close()

if __name__=='__main__':
    main()
