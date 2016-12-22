# author: nifannn
# --------------------------------
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pymysql.cursors
import time

# connect to mysql server
def MysqlConn():
	config = {'host':'127.0.0.1', 'user':'root', 'password':'password',
	          'db':'bilibili', 'charset':'utf8mb4', 
	          'cursorclass': pymysql.cursors.DictCursor}
	conn = pymysql.connect(**config)
	return conn

# get short url of sub categories
def filterSub(url):
	html = urlopen(url)
	bsObj = BeautifulSoup(html, 'html.parser')
	

# get all page numbers of sub category
def getPageNumber(sub):
	pass

# get url for spider
def getSURLs():
	url = 'http://www.bilibili.com/video/kichiku.html'
	return [sub +  '#!page=' + str(page)
	        for sub in filterSub(url)
	        for page in getPageNumber(sub)]

# get video id from url
def filterAvIds(url):
	pass

# get video info from id
def getAvInfo(AvId):
	pass

# update video info
def updateAvInfo(AvInfo):
	pass

# get up id from mysql
def selectUpIds():
	pass

# get up info from id
def getUpInfo(UpId):
	pass

# update up info
def updateUpInfo(UpInfo):
	pass

# scrap video info
def spiderVideoInfo():
	for surl in getSURLs():
		url = 'http://www.bilibili.com/video/' + surl
		for AvId in filterAvIds(url):
			AvInfo = getAvInfo(AvId)
			if AvInfo:
				updateAvInfo(AvInfo)

	return 1

# scrap up info
def spiderUpInfo():
	for UpId in selectUpIds():
		UpInfo = getUpInfo(UpId)
		if UpInfo:
			updateUpInfo(UpInfo)

	return 1

def main(argv):
	pass

if __name__ == '__main__':
	main(sys.argv)