import os
import requests

# 20143174 - PresentJay, INJE Univ.
# request test.py


def test(url):

    # HTTP GET Request
    req = requests.get(url)

    # Get HTML source
    html = req.text

    # Get HTTP header
    header = req.headers

    # Get HTTP Status
    status = req.status_code

    # a Result about HTTP request is be normal or not
    is_ok = req.ok

    print(is_ok)
    print(status)
