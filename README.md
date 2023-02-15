# 默认设置
- exosphere.ini
   序列号真实破解系统（sysmmc）不屏蔽、虚拟系统（emummc）屏蔽
- /atmosphere/config/override_config.ini
   默认相册直接进入，按住R进入hbmenu
- /atmosphere/config/system_settings.ini 
   usb30_force_enabled = u8!0x1	启用USB3.0
   dmnt_cheats_enabled_by_default = u8!0x0	作弊码默认停用
   dmnt_always_save_cheat_toggles = u8!0x0	不保存状态
   enable_dns_mitm = u8!0x1	启用DNS屏蔽
   add_defaults_to_dns_hosts = u8!0x1	添加默认配置到host文件
- /atmosphere/hosts/
   default.txt	默认生成配置
   emummc.txt	虚拟系统host
   sysmmc.txt   真实破解host（默认无此文件）
- /config/
   tesla/config.ini	特斯拉热键L+DDOWN+PLUS（L+十字键下+加号）
   TeslaMenu/sort.cfg	中文特斯拉排序文件
---
# 说明
## [setting.json](https://github.com/qhq/DeepSea/blob/custom/src/settings.json)
```
"clean":{
    "active": true,
    "modules": [
        "atmosphere", "hekate", "sigpatches", "fusee",
        "TegraExplorer", "NX-Shell", "Lockpick_RCM"
    ]
}
```
|参数|说明|
|:-|:-|
|clean|配置名称|
|active|配置是否激活|
|modules|打包的模块|

## [modules](https://github.com/qhq/DeepSea/tree/custom/src/modules)
```
{
    "url":["https://jits.cc/patches"],
    "file":"SigPatches.zip",
}
{
    "repo":"Atmosphere-NX/Atmosphere",
    "assetRegex":[".*atmosphere.*\\.zip"],
    "customSteps":[
        {
            "action": "createDir",
            "source": "atmosphere/contents"
        },
        {
            "action": "extract",
            "source": ".*atmosphere.*\\.zip"
        },
        {
            "action": "delete",
            "source": "switch/reboot_to_payload.nro"
        },
        {
            "action": "delete",
            "source": "",
            "fileRegex": "hekate_ctcaer_.*\\.bin"
        },
        {
            "action": "copy",
            "source": "atmosphere/config_templates/system_settings.ini",
            "destination": "atmosphere/config/system_settings.ini"
        },
        {
            "action": "copy",
            "source": "bootloader",
            "fileRegex": ".*hekate.*\\.bin",
            "destination": "bootloader/update.bin"
        },
        {
            "action": "move",
            "source": "linkalho.nro",
            "destination": "switch/linkalho/linkalho.nro"
        },
        {
            "action": "replaceText",
            "source": "atmosphere/config/system_settings.ini",
            "target": "; dmnt_cheats_enabled_by_default = u8!0x1",
            "replacement":"dmnt_cheats_enabled_by_default = u8!0x0"
        },
        {
            "action": "createToolboxJson",
            "source": "atmosphere/contents/00FF0000636C6BFF/",
            "requires_reboot": true
        }
    ]
}
```
|参数|说明|备注|
|:-|:-|:-|
|repo\|url|GitHub库名或链接|file配合url使用，指定保存文件名|
|createDir|新建目录|复制黏贴涉及目录需要先创建|
|extract|解压缩|path可指定解压缩目录|
|delete|删除文件或目录|fileRegex可正则匹配多个文件|
|copy|复制文件|fileRegex可正则匹配多个文件|
|move|移动文件|目录必须存在|
|replaceText|替换文本||
|createToolboxJson|创建Toolbox文件||
