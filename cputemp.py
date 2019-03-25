#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import MySQLdb
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

def getCpuTemp(address):
    file = open("/sys/class/thermal/thermal_zone0/temp")
    cputemp = float(file.read())/1000
    file.close()
    print "cputemp : %.3f" %cputemp
    mysqlDbCpuTemp(cputemp,address)

def mysqlDbCpuTemp(cputemp,address):
    tablename = "sensorinfo0"
    db = MySQLdb.connect(host='localhost', user="root", passwd="123456", db="sensor", charset='utf8')
    # 获取操作游标
    cursor = db.cursor()
    selectraspberrytablename = "select * from "+tablename+" where sensorAddress = '"+address+"' and sensorName ='树莓派cpu温度'"
    cursor.execute(selectraspberrytablename)
    cputemptablename = cursor.fetchall()
    try:
        result = cursor.execute("insert into "+cputemptablename[0][5]+" (Raspberry,address) VALUES ('%s','%s')" % (cputemp,address))
        db.commit()
        print result
    except Exception as e:
        db.rollback()
    # 关闭连接，释放资源
    db.close()

# 温湿度计进程
class myThreadth(threading.Thread):
    def __init__(self, interval, address):
        threading.Thread.__init__(self)
        self.interval = interval
        self.address = address

    def run(self):
        threadLock = threading.Lock()
        time_remaining = self.interval - time.time() % self.interval
        time.sleep(time_remaining)
        # 获得锁，成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        threadLock.acquire()
        getCpuTemp(self.address)
        # 释放锁
        threadLock.release()
