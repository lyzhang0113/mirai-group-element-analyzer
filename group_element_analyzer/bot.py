import os, sys
from io import BytesIO

sys.path.append(os.getcwd())

import json
import sqlite3
import string

from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config as ariadne_config,
)
from graia.ariadne.model import Friend, Group, Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import Source
from graia.ariadne.message.parser.base import MatchContent, DetectPrefix
from graia.ariadne.message.element import Plain, Image

from loguru import logger

import jieba
from zhon.hanzi import punctuation
from matplotlib import pyplot as plt
plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

import paddle
paddle.enable_static()
#jieba.enable_paddle()

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)

# Refer to https://graia.readthedocs.io/ariadne/quickstart/
app = Ariadne(
    ariadne_config(
        config["mirai"]["qq"],  # 你的机器人的 qq 号
        config["mirai"]["api_key"],  # 填入 VerifyKey
        HttpClientConfig(host=config["mirai"]["http_url"]),
        WebsocketClientConfig(host=config["mirai"]["ws_url"]),
    ),
)

# mkdir Database Directory
if not os.path.exists('data'):
    os.makedirs('data')

excluded_words = string.punctuation + punctuation + string.whitespace + "表情"


async def analyze_message(id: int, message: str):
    words = [word for word in jieba.cut(message, use_paddle=True) if word not in excluded_words]
    logger.debug("Extracted Words: " + "/ ".join(words))

    conn = sqlite3.connect(f'data/{str(id)}.db')

    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS STAT(
    WORD   TEXT PRIMARY KEY NOT NULL,
    LENGTH INT              NOT NULL,
    COUNT  INT              NOT NULL DEFAULT 1
    );
    ''')
    conn.commit()

    for word in words:
        c.execute('''
        INSERT INTO STAT (WORD, LENGTH)
        VALUES ("%s", "%d")
        ON CONFLICT(WORD)
        DO UPDATE SET COUNT=COUNT+1
        ''' % (word, len(word)))

    conn.commit()
    conn.close()


def generate_plot(id: int):

    MIN_LENGTH = 2

    conn = sqlite3.connect(f'data/{str(id)}.db')
    c = conn.cursor()
    c.execute('''
    SELECT WORD, COUNT FROM STAT WHERE LENGTH >= "%d"
    ORDER BY COUNT DESC
    LIMIT 10
    ''' % MIN_LENGTH)
    data = c.fetchall()
    logger.debug(f"数据库查询结果：{data}")
    conn.close()

    x, y = zip(*data)

    b = BytesIO()
    plt.bar(x, y)
    plt.title("当前群成分柱状图")
    plt.savefig(b, format="png")
    plt.clf()
    plt.close()
    return b.getvalue()


# @app.broadcast.receiver("FriendMessage")
# async def friend_message_listener(app: Ariadne, friend: Friend):
#    await app.send_message(friend, MessageChain([Plain("Hello, World!")]))
#    # 实际上 MessageChain(...) 有没有 "[]" 都没关系

@app.broadcast.receiver("GroupMessage")
async def analyze_content(group: Group, message: MessageChain):
    # Extract Plain Words from Message
    plain_texts = ''.join([text.text for text in message[Plain]])
    if plain_texts == "" or plain_texts == '查看群成分': return
    await analyze_message(group.id, plain_texts)


@app.broadcast.receiver("GroupMessage", decorators=[MatchContent('查看群成分')])
async def generate_plot_listener(app: Ariadne, group: Group, message: MessageChain):
    img = generate_plot(group.id)
    await app.send_message(group, Image(data_bytes=img))


Ariadne.launch_blocking()
