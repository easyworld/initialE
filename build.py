import src.scripts.gh as GH, src.scripts.fs as FS, src.scripts.dl as DL
import argparse, json, os, importlib, shutil
from pathlib import Path
from distutils.dir_util import copy_tree

# 递归实现多重for循环的函数
def fn(_dict, depth):
    for k, v in _dict.items():
        if depth == 1:
            yield k, v
        else:
            yield from ((k, *q) for q in fn(v, depth - 1))
            
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="TeamNeptune's DeepSea build script.")
    requiredNamed = parser.add_argument_group('Options required to build a release candidate')
    requiredNamed.add_argument('-v', '--version', help='DeepSea version tag', required=True)
    requiredNamed.add_argument('-gt', '--githubToken', help='Github Token', required=True)
    args = parser.parse_args()

    try:
        with open(Path.joinpath(Path.cwd(), "src", "settings.json")) as json_file:
            settings = json.load(json_file)
    except:
        print("Could not load Package.")
        exit()

    shutil.rmtree("tmp", ignore_errors=True)
    gh = GH.GH(args.githubToken)
    dl = DL.DL()
    fs = FS.FS()
    
    infos = []

    for packageName in settings["packages"]:
        packageObj = settings["packages"][packageName]
        if packageObj["active"] == True:
            print("=== packageName: " + packageName + " ===")
            for moduleName in packageObj["modules"]:
                downloadedFiles = None
                if fs.doesFilesExist(False, "src/modules/"+moduleName+".json"):
                    module = fs.getJson(False, "src/modules/"+moduleName+".json")
                    if not fs.doesFolderExist(True, moduleName):
                        dlPath = fs.createDirs(moduleName)
                        if "repo" in module:
                            print("Downloading: " + module["repo"])
                            downloadedFiles = gh.downloadLatestRelease(module, dlPath)
                        if "url" in module:
                            print("Downloading: " + module["file"])
                            downloadedFiles4Url = dl.downloadUrl(module, dlPath)

                        for customStep in module["customSteps"]:

                            if customStep["action"] == "createDir":
                                print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                fs.createDir(moduleName, customStep["source"])
                            
                            if customStep["action"] == "extract":
                                print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                if "path" in customStep:
                                    fs.extract(moduleName, customStep["source"], customStep["path"])
                                else:
                                    fs.extract(moduleName, customStep["source"])

                            if customStep["action"] == "delete":
                                # print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                # fs.delete(moduleName, customStep["source"])
                                if "fileRegex" in customStep:
                                    print("- custom step: " + customStep["action"] + " -> " + customStep["fileRegex"])
                                    fs.delete(moduleName, customStep["source"], customStep["fileRegex"])
                                else:
                                    print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                    fs.delete(moduleName, customStep["source"])

                            if customStep["action"] == "copy":
                                if "fileRegex" in customStep:
                                    print("- custom step: " + customStep["action"] + " -> " + customStep["fileRegex"])
                                    fs.copy(moduleName, customStep["source"], customStep["destination"], customStep["fileRegex"])
                                else:
                                    print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                    fs.copy(moduleName, customStep["source"], customStep["destination"])

                            if customStep["action"] == "move":
                                print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                fs.move(moduleName, customStep["source"], customStep["destination"])

                            if customStep["action"] == "replaceText":
                                print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                fs.replaceText(moduleName, customStep["source"], customStep["target"], customStep["replacement"])

                            if customStep["action"] == "createToolboxJson":
                                print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                fs.createToolboxJson(moduleName, customStep["source"], customStep["requires_reboot"] )
                    else:
                        if "repo" in module:
                            print("Already downloaded: " + module["repo"])
                        if "url" in module:
                            print("Already downloaded: " + module["file"])

                    outPath = str(fs.createDirs("switch_out"))
                    # print(outPath)
                    shutil.copytree(str(Path(Path.joinpath(fs.workdir, moduleName))), str(Path(Path.joinpath(fs.workdir, "switch_out"))), dirs_exist_ok=True)
                    # fs.copy("", str(Path(Path.joinpath(fs.workdir, moduleName))), outPath)
                else:
                    print("module file does not exist")
                if downloadedFiles != None:
                    infos.append({moduleName:downloadedFiles})
            shutil.copytree(str(Path(Path.joinpath(Path.cwd(), "assets"))), str(Path(Path.joinpath(fs.workdir, "switch_out"))), dirs_exist_ok=True)
            # fs.copy("", str(Path.joinpath(Path.cwd(), "assets", "boot.ini")), str(Path(Path.joinpath(fs.workdir, "switch_out","boot.ini"))))
            # fs.copy("", str(Path.joinpath(Path.cwd(), "assets", "exosphere.ini")), str(Path(Path.joinpath(fs.workdir, "switch_out","exosphere.ini"))))
            print("Zipping package: " + "atmosphere-"+packageName+"_v"+settings["version"])
            shutil.make_archive("atmosphere-"+packageName+"_v"+settings["version"],'zip',outPath)
            fs.delete("",outPath)

        else:
            print("package inactive")
    print(infos)
    cmd = ""
    for e in infos:
        # print(list(e.keys())[0])
        for item in e:
            # print("key",item)
            cmd = cmd + "|" + item
            for key, value in e[item].items():
                # print(key,value)
                cmd = cmd + "|" + value
        cmd = cmd + "|\n"
    # print(cmd)
    try:
        with open(Path.joinpath(Path.cwd(), "", "CHANGELOG.md"), '+') as f:
            c = f.read()
            print(c)
            f.write("## 版本信息\n|:-|:-|:-|\n" + cmd + "\n" + c)

    except Exception as e:
        print(e.args)
        exit()
