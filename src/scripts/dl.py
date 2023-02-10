from pathlib import Path
import urllib.request
import re

class DL():
    def __init__(self):

    def downloadUrl(self, moduleJson, downloadPath):

        downloadedFiles = []

        for url in moduleJson["url"]:
            try:
                urllib.request.urlretrieve(url, downloadFilePath)
            except:
                print("无法获取: ", url)
                return

            downloadFilePath = Path.joinpath(downloadPath, moduleJson["file"])
            urllib.request.urlretrieve(url, downloadFilePath)

