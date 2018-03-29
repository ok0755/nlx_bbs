#coding=utf-8
from gevent import monkey,pool
monkey.patch_all()
import os
import gevent
from lxml import etree
import urllib2
import time

jobs=[]
links=[]
p=pool.Pool(100)
urls=[]

f=open('d:\\nlx.txt','w')

#写入详细内容
def write_detail(url):
    res=urllib2.urlopen(url)
    r=res.read()
    res.close()
    html=etree.HTML(r)
    title=html.xpath('//title//text()')
    result=html.xpath('//div[@class="viewbox"]//text()')
    profile=html.xpath('//div[@class="profile"]//text()')
    text=''.join(result)
    f.write(title[0].encode('utf-8')+ '\n')
    f.write(profile[0].encode('utf-8') + '\r\n')
    f.write(text.encode('utf-8'))
    f.write('\n')

#分页链接地址
def get_pages(i):
    ur='http://www.nlx.gov.cn/inter/?tid=&pages=%d'%i
    html=urllib2.Request(ur)
    html=urllib2.urlopen(html)
    read=html.read()
    txt=etree.HTML(read)
    results=txt.xpath('//td[@id="title"]//a/@href')
    for result in results:
        yield result   #目标url

root_url='http://www.nlx.gov.cn/inter/'
for i in range(1,11):   #起始页
    for ur in get_pages(i):
        u=root_url+ur   #接接完整网址
        p.spawn(write_detail,u)
f.close()