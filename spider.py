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

# scrap video info
def spiderVideoInfo():
	for url in getURLs():
		for AvId in filterAvIds():
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

