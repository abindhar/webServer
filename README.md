# Information

A simple multithreaded webserver that serves files. Supports following operations:
1. GET file_path: Returns content of the file_path relative to the directory the server was started on.
2. GET dir_path: Returns contents of the directory relative to the directory the server was started on.

This HTTP file server processes incoming requests using multithreading. This enables multiple simultaneous connections to the webserver for efficient operations.

# Usage

To start the server from command line:
$ python3 webserver.py

The server listens on port 8080 for incoming requests. To specify another port use cli argument --port. For cli help use -h.

# Testing

The test.py file has several test cases.
1. GET requests including testing HTTP response codes, 200 and 404.
2. Testing response content is as expected.
3. Sequential vs Concurrent Execution time: The server must support several concurrent users/requests. A comparison of 20 sequential vs concurrent requests to the server is included in the test cases.

# Testing Usage

To run tests from command line:
$ pytest test.py -s
