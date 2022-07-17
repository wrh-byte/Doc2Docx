from pathlib import Path

import requests
import os
import aiohttp
import asyncio


def request_zip(url):
    rc = requests.get(url)
    # 请求链接后保存到链接变量 rc 中
    with open("Download_test.jpg", 'wb') as fout:
        # rc.content 写入文件
        fout.write(rc.content)


def download_bigData(url):
    # stream = True 设置为流读取
    rg = requests.get(url, stream=True)
    with open("Download_bigTest.jpg", "wb") as fout:
        for chunk in rg.iter_content(chunk_size=256):
            # 以256个字节为一块，读取文件
            if chunk:
                # 如果chunk不为空
                fout.write(chunk)


async def job(session, url, dirs_name):
    # 声明为异步函数
    name = url.split('/')[-1]
    # 获得名字
    img = await session.get(url)
    # 触发到await就切换，等待get到数据
    img_code = await img.read()
    # 读取内容
    save_path = 'DownLoadFile//' + dirs_name
    if Path(save_path).exists() is False:
        os.makedirs(save_path)
    with open(str('DownLoadFile//' + dirs_name + '//' + name), "wb") as fout:
        # 写入文件
        fout.write(img_code)
    return str(url)


async def main(loop, url, list_len, dirs_name):
    async with aiohttp.ClientSession() as session:
        # 建立会话 session
        tasks = [loop.create_task(job(session, url[_], dirs_name)) for _ in range(list_len)]
        # 建立所有任务
        finshed, unfinshed = await asyncio.wait(tasks)
        # 触发await，等待任务完成
        all_results = [r.result() for r in finshed]
        # 获取所有结果
        print("ALL RESULTS:" + str(all_results))


def loopUrlFiles(file_list):
    for dirs_name in file_list:
        with open('UrlFile//' + dirs_name + '.txt', 'r', encoding='utf8') as file:
            urls = file.readlines()

        url_lst = []
        for url in urls:
            new_url = url.replace('\n', '')
            if new_url != '':
                url_lst.append(new_url)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop, url_lst, len(url_lst), dirs_name))


if __name__ == '__main__':
    url_files = ['约尔']
    loopUrlFiles(url_files)
