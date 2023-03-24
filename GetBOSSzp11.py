
"""
数据获取
数据提取
数据存储
"""
import pandas as pd


import time
import datetime
import requests
from lxml import etree
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome import webdriver

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from time import sleep



url = r"https://youle.zhipin.com/interview-questions?sortType=1&code=180199"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
# # 构建客户端
driver = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)
# 打开地址
driver.get(url)
time.sleep(5)
print('我要开始了')
text_question = []
text_post = []
tp=0
while True:
    page_source = driver.page_source
    html_etree= etree.HTML(page_source)
    msge_list = html_etree.xpath('//ul[contains(@class, "content-card-list")]/li[contains(@class, "wrap")]')
    # count=0
    for msge in msge_list:
        msge_question = msge.xpath('./div/main/div/div[1]/text()')
        msge_post = msge.xpath('./div/main/div[2]/text()')
        if msge_question and msge_post != 0:
            text_question.append(msge_question[0])
            text_post.append(msge_post[0])
    driver.refresh()  # 每次获取后刷新页面 注意sleep一会
    sleep(2)
    tp+=1
    if tp ==10000:
        break

# print(text_question)
# print(text_post)

print('结束啦')

driver.close()


df = pd.DataFrame(data=text_question,columns=(['面试问题']))
df['岗位'] = text_post
df.to_excel('金融_投融资.xlsx')


