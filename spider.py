
# --------------------------------
import sys
from bs4 import BeautifulSoup
import requests
import re
import pymysql.cursors
import time
from math import ceil

# connect to mysql server
def MysqlConn():
	config = {'host':'127.0.0.1', 'user':'root', 'password':'password',
	          'db':'bilibili', 'charset':'utf8mb4', 
	          'cursorclass': pymysql.cursors.DictCursor}
	conn = pymysql.connect(**config)
	return conn


# get current time
def getNowTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# get sub ids 
def getSubIds():
	url = 'http://www.bilibili.com/video/kichiku.html'
	html = requests.get(url)
	soup = BeautifulSoup(html.content.decode('utf-8'), 'html.parser')
	text = soup.find('div', {'class':'b-page-body'}).script.get_text()
	return [int(tid) for tid in re.findall('[0-9]+', text)[1:]]

# get max page number from sub id
def getMaxPageNumber(SubId):
    url = 'http://api.bilibili.com/archive_rank/getarchiverankbypartion'
    jsonData = requests.get(url, {'tid':SubId}).json()['data']
    count = jsonData['page']['count']
    size = jsonData['page']['size']
    return ceil(count / size)

# get video info json data
def filterAvJsonData(SubId, PageNo):
	url = 'http://api.bilibili.com/archive_rank/getarchiverankbypartion'
    return requests.get(url, {'tid':SubId,'pn':PageNo}).json()['data']['archives']

# get video info from json data
def getAvInfo(AvJsonData):
    dbmap = {'AvId': 'aid',
             'Title': 'title',
             'Sub': 'tname',
             'CreateTime': 'create',
             'Play': 'play',
             'Danmaku': 'danmaku',
             'Coin': 'coin',
             'Favorite': 'favorites',
             'UpName': 'author',
             'UpId': 'mid',
             'Duration': 'duration',
             'Share': 'share',
             'Tag': 'tags',
             'Description': 'description',
             'Reply': 'reply',
             'AvPic': 'pic',
             'AvFace': 'face'}
    AvInfo = dict()
    AvJsonData.update(AvJsonData['stat'])
    for sqlname, jsonname in dbmap.items():
        AvInfo[sqlname] = AvJsonData[jsonname]
    AvInfo['Tag'] = '|'.join(AvInfo['Tag'])
    return AvInfo

# update video info
def updateAvInfo(AvInfo):
	conn = MysqlConn()
    try:
        with conn.cursor() as cursor:
            sqlname = "REPLACE INTO Guichu_Video "
            colname = '(AvId, Title, Sub, UpId, UpName, CreateTime, Play, Danmaku, Coin, Favorite, Reply, Share, Duration, Tag, Description, AvPic, UpFace, ScrapedTime) '
            sql = sqlname + colname + 'VALUES (' + '%s,' * 17 + '%s)'
            value = (AvInfo['AvId'],AvInfo['Title'],AvInfo['Sub'],AvInfo['UpId'],
                     AvInfo['UpName'],AvInfo['CreateTime'],AvInfo['Play'],AvInfo['Danmaku'],
                     AvInfo['Coin'],AvInfo['Favorite'],AvInfo['Reply'],AvInfo['Share'],
                     AvInfo['Duration'],AvInfo['Tag'],AvInfo['Description'],AvInfo['AvPic'],
                     AvInfo['UpFace'],getNowTime())
            cursor.execute(sql, value)

        conn.commit()
    except pymysql.err.InternalError as e:
        print(e)
    except:
        print('update Video Info error, Id:' + str(AvInfo['AvId']))
    finally:
        conn.close()

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
		for PageNo in range(1, getMaxPageNumber(SubId) + 1):
		    for AvJsonData in filterAvJsonData(SubId, PageNo):
			    AvInfo = getAvInfo(AvJsonData)
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