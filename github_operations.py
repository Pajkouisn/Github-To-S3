import wget
import urllib2
import json

def list_content(repository_url = None):
    return json.loads(urllib2.urlopen(repository_url).read())

def download_locally(url, local_path):
    #   Download the file from github.
    wget.download(url, local_path)