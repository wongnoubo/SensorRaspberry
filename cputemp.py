#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getCpuTemp(address):
    file = open("/sys/class/thermal/thermal_zone0/temp")
    cputemp = float(file.read())/1000
    file.close()
    print "cputemp : %.3f" %cputemp
    mysqlDbCpuTemp(cputemp,"RaspberryCpuTempTable0",address)

def getCpuTempInterval():
    cputempthread = threading.Timer(10,getCpuTemp,["客厅"])#需要查一下怎么传入String参数，int类型的参数是直接用个方括号括起来就可以
    cputempthread.start()

def mysqlDbCpuTemp(cputemp,tablename,address):
    db = MySQLdb.connect(host='119.23.248.55', user="root", passwd="123456", db="sensor", charset='utf8')
    # 获取操作游标
    cursor = db.cursor()
    try:
        result = cursor.execute("insert into "+tablename+" (temperature,address) VALUES ('%s','%s')" % (cputemp,address))
        db.commit()
        print result
    except Exception as e:
        db.rollback()
    # 关闭连接，释放资源
    db.close()