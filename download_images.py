import urllib.error
from multiprocessing.pool import ThreadPool
from urllib.request import urlretrieve
import urllib.parse

from Application.Misc.thread import DatabaseThread
from Application.Misc.dotenv_manager import DotEnv

data = DotEnv()


class DownloadImages:
    PATH = "Assets//Products//"

    def __init__(self, lock: bool = True):
        super(DownloadImages, self).__init__()
        self.lock = not lock

    def download(self):
        if self.lock:
            self.thread = DatabaseThread(data.get("DPWloadDictionary"), self.threaded_downloading)
            self.thread.run()

    def threaded_downloading(self, items):
        ThreadPool().imap(self.download_image, [url for _, url in items])

    def download_image(self, url: str):
        try:
            urlretrieve(url, self.PATH + url.rsplit("/", 1)[1])
        except urllib.error.HTTPError:
            print("downloading image error", url)
            pass
