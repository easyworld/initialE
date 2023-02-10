from pathlib import Path
import urllib.request
import re

class DL():
    def __init__(self):
        self.name = "下载链接"

    def downloadUrl(self, moduleJson, downloadPath):
        for url in moduleJson["url"]:
            try:
                downloadFilePath = Path.joinpath(downloadPath, moduleJson["file"])
                urllib.request.urlretrieve(url, downloadFilePath)
            except:
                print("无法获取: ", url)
                return

            urllib.request.urlretrieve(url, downloadFilePath)

