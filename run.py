# coding: utf-8
# @久辞: 3547539370


import os
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor


def main():
    main_url = 'https://wallhaven.cc/search?q=id%3A711&sorting=random&ref=fp&seed=r36jaL&page'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54 '
    }
    pages = input('请输入获取页码>>>')
    for page in range(1, int(pages) + 1):
        main_urls = main_url + f'={page}'
        temp_urls = get_all_img_url(main_urls, headers)
        # 通过跳转的url拿到图片的url
        print('下载开始'.center('-', 125))
        for img_urls in temp_urls:
            img_url = get_img_url(img_urls, headers)
            for url in img_url:
                with ThreadPoolExecutor(20) as start:
                    start.submit(downloads_img, url, headers)
        print('下载完毕'.center('-', 125))


def get_img_url(img_url, headers):
    r = requests.get(img_url, headers=headers)
    r.encoding = 'utf-8'
    et = etree.HTML(r.text)
    url = et.xpath('//*[@id="wallpaper"]/@src')
    return url


# 成功拿到跳转页面的url
def get_all_img_url(main_urls, headers):
    # 拿到每页的源代码
    res = requests.get(main_urls, headers=headers)
    res.encoding = 'utf-8'
    et = etree.HTML(res.text)
    # 提取图片的跳转页url
    list_urls = et.xpath('//section/ul/li/figure/a/@href')
    return list_urls


def downloads_img(url, headers):
    img_content = requests.get(url, headers=headers).content
    img_name = str(url).split('/')[-1]
    with open(os.getcwd() + f'\pictures\{img_name}', mode='wb') as file:
        file.write(img_content)
        print(f'{img_name}下载成功')


if __name__ == '__main__':
    main()
