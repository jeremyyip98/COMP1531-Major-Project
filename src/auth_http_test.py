import json
import requests
import urllib
import pytest

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"


def test_register_valid():
    payload = requests.post(f"{BASE_URL}/set", json={
        "email" : "test@gmail.com",
        "password" : "password",
        "name_first" : "First",
        "name_last" : "Last"
    })

