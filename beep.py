#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import camera
import threading
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

HCSRPORT = 18  # GPIO12

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(HCSRPORT, GPIO.IN)

def detct():
    time.sleep(1)
    if GPIO.input(HCSRPORT) == True:
        print "Someone is closing!"
        ishumen=1
        mysqlDbHcsr(ishumen,"客厅")
        camera.camera();
    else:
        print "No anybody!"
        ishumen=0
        mysqlDbHcsr(ishumen,"客厅")

def mysqlDbHcsr(ishumen,address):
    tablename = "sensorinfo0"
    db = MySQLdb.connect(host='localhost', user="root", passwd="123456", db="sensor",charset='utf8')
    # 获取操作游标
    cursor = db.cursor()
    selecthumentablesql = "select * from "+tablename+" where sensorAddress = '"+address+"' and sensorName ='红外人体传感器'"
    cursor.execute(selecthumentablesql)
    humentablename = cursor.fetchall()
    try:
        result = cursor.execute("insert into "+humentablename[0][5]+" (humen,address) VALUES ('%s','%s')" % (ishumen, address))
        db.commit()
        print result
    except Exception as e:
        db.rollback()
    # 关闭连接，释放资源
    db.close()

#线程相关
class cameraThreadth(threading.Thread):
    def __init__(self, interval):
        threading.Thread.__init__(self)
        self.interval = interval

    def run(self):
        threadLock = threading.Lock()
        time_remaining = self.interval - time.time() % self.interval
        time.sleep(time_remaining)
        # 获得锁，成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        threadLock.acquire()
        init()
        detct()
        # 释放锁
        threadLock.release()