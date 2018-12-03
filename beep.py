#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import camera
import threading
import MySQLdb

HCSRPORT = 18  # GPIO12

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(HCSRPORT, GPIO.IN)

def detct():
    time.sleep(1)
    personflag=0
    if GPIO.input(HCSRPORT) == True:
        print "Someone is closing!"
        camera.camera()
        personflag = 1
        mysqlDbHcsr(personflag,"HcsrSensor1","儿童房")
        return personflag
    else:
        print "No anybody!"
        return personflag

#10s检查一次
def hcsrInterval():
    init()
    cputempthread = threading.Timer(6,detct)
    cputempthread.start()

def mysqlDbHcsr(personflag,tablename,address):
    db = MySQLdb.connect(host='119.23.248.55', user="root", passwd="123456", db="sensor",charset='utf8')
    # 获取操作游标
    cursor = db.cursor()
    createtablesql = "CREATE TABLE if not exists "+tablename+" (`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`personflag` varchar(50) DEFAULT NULL, "+ address+" varchar(50) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cursor.execute(createtablesql)
    try:
        result = cursor.execute("insert into "+tablename+" (personflag,address) VALUES ('%s','%s')" % (personflag,address))
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