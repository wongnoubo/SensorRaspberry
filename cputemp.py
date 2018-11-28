#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import MySQLdb

def getCpuTemp(address):
    file = open("/sys/class/thermal/thermal_zone0/temp")
    cputemp = float(file.read())/1000
    file.close()
    print "cputemp : %.3f" %cputemp
    #jsondata = tojson.cpuTempToJson(cputemp)
    mysqlDbCpuTemp(cputemp,"cputemp1",address)

def getCpuTempInterval():
    cputempthread = threading.Timer(10,getCpuTemp,["主卧"])#需要查一下怎么传入String参数，int类型的参数是直接用个方括号括起来就可以
    cputempthread.start()

def mysqlDbCpuTemp(cputemp,tablename,address):
    db = MySQLdb.connect(host='119.23.248.55', user="root", passwd="123456", db="sensor")
    # 获取操作游标
    cursor = db.cursor()
    createtablesql = "CREATE TABLE if not exists "+tablename+" (`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`cputemp` varchar(50) DEFAULT NULL, "+ address+" varchar(50) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cursor.execute(createtablesql)
    try:
        result = cursor.execute("insert into "+tablename+" (cputemp,address) VALUES ('%s','%s')" % (cputemp,address))
        db.commit()
        print result
    except Exception as e:
        db.rollback()
    # 关闭连接，释放资源
    db.close()