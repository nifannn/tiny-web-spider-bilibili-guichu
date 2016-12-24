
# --------------------------------
import sys
from bs4 import BeautifulSoup
import requests
import json
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

# get sub ids 
def getSubIds():
	url = 'http://www.bilibili.com/video/kichiku.html'
	html = requests.get(url)
	soup = BeautifulSoup(html.content.decode('utf-8'), 'html.parser')


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
	for SubId in getSubIds():
		for page in xrange(1, getMaxPageNumber(SubId) + 1):
		    for AvId in filterAvIds(SubId, page):
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