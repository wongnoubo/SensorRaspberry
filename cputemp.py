#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import MySQLdb

import tojson

def getCpuTemp():
    file = open("/sys/class/thermal/thermal_zone0/temp")
    cputemp = float(file.read())/1000
    file.close()
    print "cputemp : %.3f" %cputemp
    jsondata = tojson.cpuTempToJson(cputemp)
    mysqlDbCpuTemp(jsondata)

def getCpuTempInterval():
    cputempthread = threading.Timer(10,getCpuTemp)
    cputempthread.start()

def mysqlDbCpuTemp(jsondata):
    db = MySQLdb.connect(host='119.23.248.55', user="root", passwd="123456", db="sensor")
    # 获取操作游标
    cursor = db.cursor()
    createtablesql = "CREATE TABLE if not exists `cputemp` (`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`cputemp` varchar(50) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cursor.execute(createtablesql)
    try:
        result = cursor.execute("insert into cputemp (cputemp) VALUES ('%s')" % (jsondata))
        db.commit()
        print result
    except Exception as e:
        db.rollback()
    # 关闭连接，释放资源
    db.close()