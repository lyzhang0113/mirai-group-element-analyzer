# Mirai Word Frequency Counter 【群成分统计器】

一款统计群友词频并生成统计图的 Mirai QQ 机器人插件

基于
 - [Ariadne](https://github.com/GraiaProject/Ariadne)
 - [mirai-http-api](https://github.com/project-mirai/mirai-api-http)
 - [Jieba](https://github.com/fxsjy/jieba)

使用
 - [SQLite](https://www.sqlite.org/index.html)

支持：  
* [x] 分群统计词频
* [ ] 按日期筛选群成分
* [ ] 按词长度筛选群成分
* [ ] 使用paddlepaddle深度学习模型来进行分词，达到更高的准确性

## 介绍
此插件监视群友的每一条消息，在过滤表情、标点等富文本后，使用[Jieba](https://github.com/fxsjy/jieba)库对每一条纯文本进行分词后统计至SQLite数据库（数据保存至`./data`路径下）。

由于SQLite自带 **ACID** 的特性，理论上线程安全，支持高强度聊天。

统计后的数据在群友呼唤 **_查看群成分_** 后使用`matplotlib.pyplot`进行绘图并发送。


## 🔧 使用方法

提示：我开发时使用的Python版本为3.9.13

1. 部署 Mirai ，安装 mirai-http-api 插件

2. 下载本项目并使用`poetry`安装依赖:
```bash
git clone https://github.com/lyzhang0113/mirai_word_frequency_counter.git
cd mirai_word_frequency_counter
poetry install
```

3. 重命名 `config.example.json` 为 `config.json`, 更改里面的配置.  


4. 启动 bot.
```bash
poetry run python .\mirai_word_frequency_counter\bot.py
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
