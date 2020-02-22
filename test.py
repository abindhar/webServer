import os, subprocess, sys, time
import pytest
from http import HTTPStatus
import requests


def check_get_response(path, expected_status, expected_text = None):
    url = "http://localhost:8080"  + "/" + path
    if expected_status != HTTPStatus.OK and expected_text is not None:
        raise Exception('Text should not be specified when status is not 200')
    r = requests.get(url)
    assert expected_status == r.status_code
    if expected_text is not None:
        assert expected_text == r.text

def test_get():
    #check_get_response("/sampledir/", HTTPStatus.OK, '{"1.txt": "file", "10.txt": "file", "2.txt": "file", "3.txt": "file", "4.txt": "file", "5.txt": "file", "6.txt": "file", "7.txt": "file", "8.txt": "file", "9.txt": "file", "10.txt": "file"')
    #return
    check_get_response("/invalid_dir/", HTTPStatus.NOT_FOUND)
    check_get_response("/invalidfile.html", HTTPStatus.NOT_FOUND)
    check_get_response("/invalidfile.json", HTTPStatus.NOT_FOUND)
    check_get_response("/invalidfile.xml", HTTPStatus.NOT_FOUND)
    # Valid Files / Directories
    check_get_response("/sampledir/1.txt", HTTPStatus.OK, "File1")
    return
    check_get_response("dir", HTTPStatus.OK, '{"ff": "file"}')
    check_get_response('', HTTPStatus.OK, '{"dir": "directory", "ff": "file"}')