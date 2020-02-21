# Information

A simple multithreaded webserver that serves files. Supports following operations:
1. GET file_path: Returns content of the file_path relative to the directory the server was started on.
2. GET dir_path: Returns contents of the directory relative to the directory the server was started on.

This HTTP file server processes incoming requests using multithreading. This enables multiple simultaneous connections to the webserver

# Usage

To start the server from command line
python3 server.py <port>


# Authentication

Basic form of authentication for a user requesting file access in the form of basic HTTP Authentication.
Client sends a request containing a header field in the form of Authorization: Basic <credentials>
