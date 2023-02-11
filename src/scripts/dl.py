from pathlib import Path
import urllib.request
import re
import datetime

class DL():
    def __init__(self):
        self.name = "下载链接"

    def downloadUrl(self, moduleJson, downloadPath):

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S'
        local_time = datetime.datetime.strptime(current_time, GMT_FORMAT) + datetime.timedelta(hours=8)
        now = local_time.strftime("%Y-%m-%d %H:%M:%S")

        for url in moduleJson["url"]:
            try:
                print("- downloading: " + url)
                downloadFilePath = Path.joinpath(downloadPath, moduleJson["file"])
                urllib.request.urlretrieve(url, downloadFilePath)
            except:
                print("无法获取: ", url)
                return

            urllib.request.urlretrieve(url, downloadFilePath)

            info = {"tag":"9.9.9","last_modified":now,"url":url}
            # print(info)

        return info

