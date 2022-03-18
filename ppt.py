import requests
from bs4 import BeautifulSoup
import random
import os
import time


def getHeaders():
    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent = random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers
if not os.path.exists('./PPT/'):
    os.mkdir('./PPT/')


headers = getHeaders()
for i in range(0,10):
    url = "http://www.51pptmoban.com/e/search/result/index.php?page={}&searchid=2194".format(str(i))
    res = requests.get(url=url,headers=headers).text

    #  bs4解析数据
    # 1.使用通用爬虫解析首页，获取每个ppt的url
    soup = BeautifulSoup(res,'lxml')
    url_list = soup.select('.pptlist > dl dd')
    for dd in url_list:
        dowm_url = 'http://www.51pptmoban.com'+dd.div.a['href']

        # 对url下载的地址发送请求，获取下载页面
        res = requests.get(url=dowm_url, headers=headers).text
        soup = BeautifulSoup(res, 'lxml')

        # 新知识点
        node = soup.find('div',class_='ppt_xz')
        new_url = 'http://www.51pptmoban.com/'+node.a['href']

        # 获取名字
        div = soup.find('div',class_='title')
        # 解决乱码
        name = (div.div.h1.get_text()).encode("iso-8859-1").decode("gbk")

        # 获取到下载地址的页面之后，对下载地址的url进行请求
        res = requests.get(url=new_url, headers=headers).text
        soup = BeautifulSoup(res, 'lxml')
        dowm = soup.find('div',class_='down')
        text = dowm.a['href']
        dowm_rar_url = 'http://www.51pptmoban.com/e/DownSys/GetDown/'+''.join(text.split('/')[2:])
        ppt_date = requests.get(url=dowm_rar_url, headers=headers).content
        path = './PPT/'+name+'.zip'
        try:
            with open(path,'wb') as fp:
                fp.write(ppt_date)
            print("%s爬取完成！"%name)
            time.sleep(1)
        except:
            print('无法爬取%s!'%name)
            continue

    break
    print('第一页爬取完成！')
    time.sleep(5)  # 减慢爬取速度，防止被发现






