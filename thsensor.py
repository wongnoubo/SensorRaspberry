#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import MySQLdb
import threading

import tojson

def _do_click_V1001_TEMPERATURES(tablename,TEMPERPORT):
    data = []
    j = 0
    GPIO.setmode(GPIO.BCM)
    time.sleep(1)
    GPIO.setup(TEMPERPORT, GPIO.OUT)
    GPIO.output(TEMPERPORT, GPIO.LOW)
    time.sleep(0.02)
    GPIO.output(TEMPERPORT, GPIO.HIGH)
    GPIO.setup(TEMPERPORT, GPIO.IN)
    while GPIO.input(TEMPERPORT) == GPIO.LOW:
        continue
    while GPIO.input(TEMPERPORT) == GPIO.HIGH:
        continue
    while j < 40:
        k = 0
        while GPIO.input(TEMPERPORT) == GPIO.LOW:
            continue
        while GPIO.input(TEMPERPORT) == GPIO.HIGH:
            k += 1
            if k > 100:
                break
        if k < 8:
            data.append(0)
        else:
            data.append(1)
        j += 1
    print "sensor is working."

    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]

    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    check = 0

    for i in range(8):
        humidity += humidity_bit[i] * 2 ** (7 - i)
        humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
        temperature += temperature_bit[i] * 2 ** (7 - i)
        temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
        check += check_bit[i] * 2 ** (7 - i)
    tmp = humidity + humidity_point + temperature + temperature_point

    if check == tmp:
        print"temperature : ", temperature, ", humidity : ", humidity
        jsondata = tojson.THresultToJson(temperature,humidity)
        mysqlDbthvalue(tablename,jsondata)
    else:
        print "wrong"
       # print "temperature : ", temperature, ", humidity : ", humidity, " check : ", check, " tmp : ", tmp
    #GPIO.cleanup()

#连接数据库
def mysqlDbthvalue(tablename,jsondata):
    # 建立和数据库的连接
    db = MySQLdb.connect(host='119.23.248.55', user="root", passwd="123456", db="sensor")
    # 获取操作游标
    cursor = db.cursor()
    createtablesql="CREATE TABLE if not exists  "+tablename+" ( `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, `thvalue` varchar(50) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cursor.execute(createtablesql)
    # 执行sql
    try:
        result = cursor.execute("insert into "+tablename+" (thvalue) VALUES ('%s')" % (jsondata))
        db.commit()
        print result
    except Exception as e:
        db.rollback()
    # 关闭连接，释放资源
    db.close()

#温湿度计进程
class myThreadth(threading.Thread):
    def __init__(self, threadID, TEMPERPORT, interval,tablename):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.TEMPERPORT = TEMPERPORT
        self.interval = interval
        self.tablename = tablename

    def run(self):
        threadLock = threading.Lock()
        time_remaining = self.interval - time.time() % self.interval
        time.sleep(time_remaining)
        print "Starting:",self.TEMPERPORT
        # 获得锁，成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        threadLock.acquire()
        _do_click_V1001_TEMPERATURES(self.tablename,self.TEMPERPORT)
        # 释放锁
        threadLock.release()