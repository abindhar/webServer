"""
Testsuite
1. For testing HTTP Status and Response text body to validate server setup and functionality
2. For comparing sequential vs concurrent accesses
"""
import pytest
import os, subprocess, sys, time
import asyncio, concurrent.futures
from http import HTTPStatus
import requests

def check_get_response(path, expected_status, expected_text = None):
    """Compare HTTP status code and response
    """
    url = "http://localhost:8080"  + "/" + path
    if expected_status != HTTPStatus.OK and expected_text is not None:
        raise Exception('Text should not be specified when status is not 200')
    r = requests.get(url)
    assert expected_status == r.status_code
    if expected_text is not None:
        assert expected_text == r.text

def test_get():
    """Sanity test cases for the server
    """
    # Invalid Files / Directory Access
    check_get_response("/invalid_dir/", HTTPStatus.NOT_FOUND)
    check_get_response("/invalidfile.html", HTTPStatus.NOT_FOUND)
    check_get_response("/invalidfile.json", HTTPStatus.NOT_FOUND)
    check_get_response("/invalidfile.xml", HTTPStatus.NOT_FOUND)
    # Valid Files / Directories Access and Response text comparison
    check_get_response("/sampledir/1.txt", HTTPStatus.OK, "File1")
    check_get_response("/sampledir/2.txt", HTTPStatus.OK, "File2")
    check_get_response("/samplejson/", HTTPStatus.OK, '{"example_1.json": "file", "example_2.json": "file"}')
    check_get_response("/samplexml", HTTPStatus.OK, '{"example1.xml": "file"}')
    check_get_response("/articles/a/b/a/", HTTPStatus.OK, '{"Abatasa.html": "file"}')
    check_get_response("/sampledir/", HTTPStatus.OK, '{"1.txt": "file", "10.txt": "file", "2.txt": "file", "3.txt": "file", "4.txt": "file", "5.txt": "file", "6.txt": "file", "7.txt": "file", "8.txt": "file", "9.txt": "file"}')
    print("PASSED: All test_get() tests")

def test_sequential_access():
    """Time Sequential GET requests to the server
    """
    url = "http://localhost:8080"  + "/" + "articles/a/b/a/Abatasa.html"
    start = time.time()
    num_requests = 20
    for _ in range(num_requests):
        r = requests.get(url)
    elapsed = round(time.time() - start, 3)
    print("PASSED: All test_sequential_access() tests")
    print(f"Time taken for {num_requests} serial accesses: {elapsed}")
    

async def concurrent_requests():
    """Concurrent request generator
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        url = "http://localhost:8080"  + "/" + "articles/a/b/a/Abatasa.html"
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(executor, requests.get, url) for _ in range(20)]
        await asyncio.gather(*futures)

def test_concurrent_access():
    """Time concurrent get requests to the server
    """
    num_con_requests = 20
    loop = asyncio.get_event_loop()
    start = time.time()
    loop.run_until_complete(concurrent_requests())
    elapsed = round(time.time() - start, 3)
    print("PASSED: All test_concurrent_access() tests")
    print(f"Time taken for {num_con_requests} concurrent accesses: {elapsed}")
    