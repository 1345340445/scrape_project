#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 10:20:17 2018

@author: muqingli
"""

# -*- coding:utf-8 -*-
# import urllib.request as request
# import urllib.parse
# import re
#用来创建excel文档并写入数据
import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver


#获取网页的源码
def get_content(driver, url):
    #网址
    #打开网址
    driver.get(url)
    #读取源代码并转为unicode
    #html = a.text
    return driver.page_source

#正则匹配要爬取的内容
def get(html):
    #正则匹配式
    soup = BeautifulSoup(html, 'html.parser')
    jobs = soup.find_all('div', class_="searchResultItemDetailed")
    items = list()
    for job in jobs:
        url = job.find('a')['href'].strip()
        try:
            job_name = job.find('a').get_text().strip()
        except AttributeError:
            job_name = ''
        try:
            company_name = job.find('p', class_="searchResultCompanyname").find('span').get_text().strip()
        except AttributeError:
            company_name = ''
        try:
            job_desc = job.find('p', class_="searchResultJobdescription").get_text().strip()
        except AttributeError:
            job_desc = ''
        try:
            release_time = job.find_all('span', class_="searchResultKeyval")[1].find('em').text
        except AttributeError:
            release_time = ''
        result = (url, job_name, company_name, release_time, job_desc)
        items.append(result)
    #reg = re.compile(r'class="searchResultJobName">.*?<a joburl href="//(.*?)" class="fl __ga__fullResultcampuspostname_clicksfullresultcampuspostnames_001">(.*?)</a>.*?<p class="searchResultCompanyname"><span>(.*?)</span>.*?<span>发布时间：<em>(.*?)</em></span>.*?职责描述：<span>(.*?)</span>',re.S)
    #进行匹配
    #items = re.findall(reg,html)
    #print(items)
    #计算匹配到的数目（一整条记录算一个）
    items_length = len(items) 
    return items,items_length

#爬取到的内容写入excel表格
def excel_write(items,index):
    #将职位信息写入excel,item为tuple元组
    for item in items:
        #共五个信息，写五列
        for i in range(0,5):
            #print item[i]
            #.write（行，列，数据）
            ws.write(index,i,item[i])
        #每成功写入一条就输出对应的行编号
        print(index)
        #index+1，写下一行
        index+=1
    return index
        

##写入表头信息
##excel名称
#newTable="智联招聘岗位爬虫结果.xls"
##创建excel文件，声明编码为utf-8
#wb = xlwt.Workbook(encoding='utf-8')
##创建表格
#ws = wb.add_sheet('sheet1')
##表头信息
#headData = ['url','职位','公司','发布时间','职责描述']


#urlhead = 'https://xiaoyuan.zhaopin.com'


#爬取信息
#items,items_length = get(get_content(driver, url))
#写入excel
#excel_write(items,index)
#保存excel


def get_next_url(driver):
    #driver.get(url)
    page = driver.find_elements_by_xpath("//span[@class='font12 pageNext']")
    #print(page)
    driver.execute_script('arguments[0].scrollIntoView();', page[-1])
    #next_page = driver.find_elements_by_xpath('//ul[@class="npage fr"]/li')[-1].find_elements_by_xpath('a')[-1]
    next_page = driver.find_elements_by_xpath("//span[@class='font12 pageNext']")[0]
    #print(next_page)
    next_page.click()
    return driver.page_source
    
#跳转下一页
#get_nextpage(driver, url)  
#page = driver.find_elements_by_xpath("//div[@class='flod-button']")
#print(page)
#driver.execute_script('arguments[0].scrollIntoView();', page[-1])
#page.click()#拖动到可见的元素去
# first page
if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
    driver = webdriver.Chrome('/Users/muqingli/Downloads/chromedriver',chrome_options = options)
    #excel名称
    newTable="智联招聘岗位爬虫结果.xls"
    #创建excel文件，声明编码为utf-8
    wb = xlwt.Workbook(encoding='utf-8')
    #创建表格
    ws = wb.add_sheet('sheet1')
    #表头信息
    headData = ['url','职位','公司','发布时间','职责描述']
    #写入表头信息
    for colnum in range(0, 5):
        ws.write(0, colnum, headData[colnum], xlwt.easyxf('font: bold on'))
    url = 'https://xiaoyuan.zhaopin.com/full/0/0_0_210500_0_0_-1_技术_1_0'
    #从第2行开始写入
    index = 1
        
    items,items_length = get(get_content(driver, url))
    index = excel_write(items,index)
    #wb.save(newTable)
    # second and the rest page
    while index < 2000: 
        items,items_length = get(get_next_url(driver))
        index = excel_write(items,index)
    
    wb.save(newTable)

