
from pathlib import Path
from github import Github
import urllib.request
import re
import datetime

class GH():
    def __init__(self, ghToken):
        self.token = ghToken
        self.github = Github(self.token)

    def downloadLatestRelease(self, moduleJson, downloadPath):
        try:
            ghRepo = self.github.get_repo(moduleJson["repo"])
        except:
            print("无法获取: ", moduleJson["repo"])
            return
        
        ghLatestTag = ghRepo.get_tags()[0]
        # print( "last tag: " + ghLatestTag.name) # v1.0
        # print( "time: " + ghLatestTag.last_modified) # Fri, 23 Oct 2020 04:21:50 GMT
        # print( "raw: " + ghLatestTag.raw_data)
        commit = ghLatestTag.commit # Commit(sha="7e700a25a6cb378d5c04d7cb3d616c14546d1c6b")
        timestamp =  commit.stats.last_modified # # Fri, 23 Oct 2020 04:21:50 GMT
       
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        local_time = datetime.datetime.strptime(timestamp, GMT_FORMAT) + datetime.timedelta(hours=8)
        now = local_time.strftime("%Y-%m-%d %H:%M:%S")
        # print("last modified: " + now)
        
        info = {"tag":ghLatestTag.name,"last_modified":now}
        print(info)
        
        releases = ghRepo.get_releases()
        if releases.totalCount == 0:
            print("无可用版本: ", moduleJson["repo"])
            return
        ghLatestRelease = releases[0]

        downloadedFiles = []

        for pattern in moduleJson["assetRegex"]:
            matched_asset = None
            for asset in ghLatestRelease.get_assets():
                if re.search(pattern, asset.name):
                    matched_asset = asset
                    break
            if matched_asset is None:
                print("未找到文件: ", pattern)
                return

            downloadFilePath = Path.joinpath(downloadPath, matched_asset.name)
            # print("downloadFilePath: ", downloadFilePath)
            urllib.request.urlretrieve(matched_asset.browser_download_url, downloadFilePath)
            downloadedFiles.append(downloadFilePath)
        
        # return downloadedFiles
        return info
