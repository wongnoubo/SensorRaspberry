#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import sys
import os
import commands
from datetime import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def camera():
    commands.getoutput("fswebcam -p YUYV -d /dev/video0 -r 640x480 /home/pi/sensor/images170/" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg")
    mysqlDbCamera()#将照片存入mysql数据库

#用来读取产生的图片
def readImg():
    #path = "f:\\img\\"
    path="/home/pi/sensor/images170/"
    path_list = os.listdir(path)
    file_dict = {}
    for i in path_list:  # 遍历所有文件
        ctime = os.stat(os.path.join(path, i)).st_ctime
        file_dict[ctime] = i  # 添加创建时间和文件名到字典
    max_ctime = max(file_dict.keys())  # 取值最大的时间
    #path_list.reverse()
    print file_dict[max_ctime]
    return file_dict[max_ctime]

def mysqlDbCamera():
    #path = "f:\\img\\"
    #path = "/home/pi/sensor/images170/"
    imglist = readImg()
    print "1" + imglist
    path = "/home/pi/sensor/images170/"
    fp = open(path+imglist,"rb")
    img = fp.read()
    fp.close()
    db = MySQLdb.connect(host='localhost', user="root", passwd="123456", db="sensor",charset='utf8')
    # 获取操作游标
    cursor = db.cursor()
   # createtablesql=""
    imgdata = MySQLdb.Binary(img)
    #n = cursor.execute("select * from img")#获取多少条数据
    #print "照片：",n
   # n = cursor.execute("select id from img")
    #print  "照片：",n
    #camerasql = "INSERT INTO img (id,imgname,imgs) VALUES(%s,%s,%s)"
    #args=(n+1,imglist[0],imgdata)
    camerasql = "INSERT INTO img (imgname,imgs) VALUES(%s,%s)"
    print "2"+imglist
    args = (imglist, imgdata)
    cursor.execute(camerasql,args)
    cursor.close()
    db.commit()
    # 关闭数据库连接
    db.close()

#从mysql中将图片拿出来
def mysqlDbOpen():
    try:
        db = MySQLdb.connect(host='119.23.248.55', user="root", passwd="123456", db="sensor")
        cursor = db.cursor()
        cursor.execute("SELECT imgs FROM img LIMIT 1")
        fout = open('huanglei.png', 'wb')
        fout.write(cursor.fetchone()[0])
        fout.close()
        cursor.close()
        db.close()
    except IOError, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
