import os
import urllib.error
from multiprocessing.pool import ThreadPool
from urllib.request import urlretrieve
import urllib.parse


TEMP = os.environ["TEMP"]
PATH = "Assets//Products//"


def threaded_downloading(urls: iter):
    ThreadPool().imap(download_image, urls)


def download_image(url: str):
    try:
        urlretrieve(url, PATH + url.rsplit("/", 1)[1])
    except urllib.error.HTTPError as e:
        print("downloading image error", url)
        pass
