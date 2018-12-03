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
    mysqlDbCpuTemp(cputemp,address)

def getCpuTempInterval():
    cputempthread = threading.Timer(10,getCpuTemp,["儿童房"])#需要查一下怎么传入String参数，int类型的参数是直接用个方括号括起来就可以
    cputempthread.start()

def mysqlDbCpuTemp(cputemp,address):
    tablename = "sensor_info"
    db = MySQLdb.connect(host='119.23.248.55', user="root", passwd="123456", db="sensor", charset='utf8')
    # 获取操作游标
    cursor = db.cursor()
    selectraspberrytablename = "select * from "+tablename+" where sensorAddress = '"+address+"' and sensorName ='树莓派cpu温度'"
    cursor.execute(selectraspberrytablename)
    cputemptablename = cursor.fetchall()
    print cputemptablename
    try:
        result = cursor.execute("insert into "+cputemptablename[0][5]+" (temperature,address) VALUES ('%s','%s')" % (cputemp,address))
        db.commit()
        print result
    except Exception as e:
        db.rollback()
    # 关闭连接，释放资源
    db.close()
