
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
	config = {'host':'127.0.0.1', 'user':'root', 'password':'passwd',
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
def getAvInfo(AvJsonData,SubId,PageNo):
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
             'UpFace': 'face'}
    
    AvInfo = dict()
    if 'access' in AvJsonData.keys():
        AvJsonData['play'] = 0
    if AvJsonData['favorites'] == -1:
        AvJsonData['favorites'] = 0
    if AvJsonData['create'] == '--':
        AvJsonData['create'] = filterAvJsonData(SubId,PageNo)[-1]['create']
    else:
        AvJsonData['create'] = getNowTime()
    
    AvJsonData.update(AvJsonData['stat'])
    for sqlname, jsonname in dbmap.items():
        AvInfo[sqlname] = AvJsonData[jsonname]
    AvInfo['Tag'] = '|'.join(AvInfo['Tag'])
    return AvInfo

# update video info
def updateAvInfo(AvInfo, SubId, PageNo):
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
        print('Id: ' + str(AvInfo['AvId']) + ' SubId: ' + str(SubId) + ' PageNo: ' + str(PageNo))
    except:
        print('update Video Info error, Id: ' + str(AvInfo['AvId']) + ' SubId: ' + str(SubId) + ' PageNo: ' + str(PageNo))
    finally:
        conn.close()

# get up id from mysql
def selectUpIds():
    conn = MysqlConn()
    with conn.cursor() as cursor:
        sql = "select UpId from Guichu_Video"
        cursor.execute(sql)
        results = cursor.fetchall()

    conn.close()
    return [list(result.values())[0] for result in results]

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
			    AvInfo = getAvInfo(AvJsonData, SubId, PageNo)
			    if AvInfo:
				    updateAvInfo(AvInfo, SubId, PageNo)

	return 1

# scrap up info
def spiderUpInfo():
	for UpId in selectUpIds():
		UpInfo = getUpInfo(UpId)
		if UpInfo:
			updateUpInfo(UpInfo)

	return 1

# get video count
def getVideoCount():
    conn = MysqlConn()
    with conn.cursor() as cursor:
        sql = "SELECT COUNT(AvId) FROM Guichu_Video"
        cursor.execute(sql)
        result = cursor.fetchone()

    conn.close()
    return list(result.values())[0]

# get up count
def getUpCount():
    pass

def main(argv):
    usage = 'Usage: python spider.py [spiderVideoInfo|spiderUpInfo|getVideoCount|getUpCount]'
    if len(argv) < 2:
        print(usage)
        exit()
    if argv[1] == 'spiderVideoInfo':
        starttime = time.time()
        spiderVideoInfo()
        endtime = time.time()
        duration = time.strftime('%H:%M:%S', time.gmtime(starttime-endtime))
        print('This operation lasts ' + duration + ' .')
        print('Currently there are ' + str(getVideoCount()) +' video records.')
    elif argv[1] == 'spiderUpInfo':
        starttime = time.time()
        spiderUpInfo()
        endtime = time.time()
        duration = time.strftime('%H:%M:%S', time.gmtime(starttime-endtime))
        print('This operation lasts ' + duration + ' .')
        print('Currently there are ' + str(getUpCount()) + ' up records.')
    elif argv[1] == 'getVideoCount':
        print('Currently there are ' + str(getVideoCount()) +' video records.')  
    elif argv[1] == 'getUpCount':
        print('Currently there are ' + str(getUpCount()) +' up records.')
    else:
        print(usage)

if __name__ == '__main__':
	main(sys.argv)