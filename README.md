# Mirai Group Element Analyzer 【群成分统计器】

一款统计群友词频并生成统计图的 Mirai QQ 机器人插件

基于
 - [Ariadne](https://github.com/GraiaProject/Ariadne)
 - [mirai-http-api](https://github.com/project-mirai/mirai-api-http)
 - [Jieba](https://github.com/fxsjy/jieba)

支持：  
* [x] 分群统计词频

## 🔧 使用方法

提示：我开发时使用的Python版本为3.9.13

1. 部署 Mirai ，安装 mirai-http-api 插件

2. 下载本项目并使用`poetry`安装依赖:
```bash
git clone https://github.com/lyzhang0113/mirai-group-element-analyzer.git
cd mirai-group-element-analyzer
poetry install
```

3. 重命名 `config.example.json` 为 `config.json`, 更改里面的配置.  


4. 启动 bot.
```bash
poetry run python .\group_element_analyzer\bot.py
```



## ⚙ 配置文件

你可以参考 `config.example.json` 来写配置文件。   


```jsonc
{
    "mirai": {
        "qq": <机器人QQ号>,
        "api_key": "<Mirai HTTP VerifyKey>",
        "http_url": "http://localhost:8080",
        "ws_url": "http://localhost:8080"
    }
}
```
