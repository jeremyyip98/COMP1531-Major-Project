"""
UNSW Comp1531 Iteration 2
user HTTP test
Jeffrey Yang z5206134
"""
import urllib #pylint: disable=unused-import
import json #pylint: disable=unused-import
import requests #pylint: disable=unused-import
import pytest #pylint: disable=unused-import

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"

def test_standup_valid():
    '''http test for standup'''
