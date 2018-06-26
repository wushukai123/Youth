#!/usr/bin/env python
# coding=utf-8
import urllib2,json,pymongo
from pymongo import MongoClient

print('连接到Mongo服务器...')

connection = MongoClient('localhost', 27017)
print('连接上了!')

tdb = connection.myBlog
YiYanTable = tdb.yiYan

header = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}

url = "https://sslapi.hitokoto.cn?encode=json"

html = urllib2.urlopen(url)

jsonContent = json.loads(html.read())

YiYan = {}
YiYan['content'] = jsonContent['hitokoto']
YiYan['type'] = jsonContent['type']
YiYan['from'] = jsonContent['from']
YiYan['creator'] = jsonContent['creator']
YiYan['created_at'] = jsonContent['created_at']
print YiYan

oneContent = jsonContent['hitokoto'].encode('utf-8')
oneType = jsonContent['type'].encode('utf-8')
oneOrigin = jsonContent['from'].encode('utf-8')
oneCreator = jsonContent['creator'].encode('utf-8')
oneCreatedAt = jsonContent['created_at'].encode('latin-1','ignore')
print oneContent
print oneType
print oneCreator
print oneCreatedAt

YiYanTable.insert_one(YiYan)

for data in YiYanTable.find():  
    print data 

print '爬取数据并插入mysql数据库完成...'