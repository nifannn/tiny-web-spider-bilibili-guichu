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
	config = {'host':'127.0.0.1', 'user':'root', 'password':'sqlkg1421',
	          'db':'bilibili', 'charset':'utf8mb4', 
	          'cursorclass': pymysql.cursors.DictCursor}
	conn = pymysql.connect(**config)
	return conn

# scrap user data
def spiderUserData():
	pass

# scrap video data
def spiderVideoData():
	pass