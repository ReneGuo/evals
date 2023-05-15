# coding: utf-8
import threading
import time
import uuid

import requests
from tqdm import tqdm

# url = "http://43.136.25.20:20018/run/chat"
model_addr = "http://101.43.162.118:20021/run/chat"
query_list = ["马化腾是谁", "北京有什么美食推荐？", "我想减肥,帮我做个计划", "白日依山尽的下一句是什么", "减肥餐的食谱"]
# model_addr = 'http://sit-cognition-api.xverse.cn/v1/dialogue/utter'
# 访问次数
m = 1


def chat(query):
    resp = requests.post(
        model_addr,
        json={
            "data": [
                query,
                None,
                "auto",
                "",
                "问题",
                "回答",
                "",
                "250",
                1,
                50,
                0.92,
                0,
                1,
                1.2,
            ]
        },
    ).json()
    print(resp)
    res = resp["data"][0][-1][-1]
    return res


# 保存结果
bar = tqdm(query_list)

for idx, query in enumerate(bar):
    data_file = open(f"gradio_test_data_{idx}.txt", 'w')
    for j in range(m):
        res = chat(query)
        data_file.write(res)
    data_file.close()
