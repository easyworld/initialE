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
|:-|-:|
|clean|配置名称|
|active|配置是否激活|
|modules|打包的模块|

## [modules](https://github.com/qhq/DeepSea/tree/custom/src/modules)
|参数|说明|备注|
|:-|:-:|-:|
|repo\|url|GitHub库名或链接|file配合url使用，指定保存文件名|
|active|配置是否激活||
|modules|打包的模块||
