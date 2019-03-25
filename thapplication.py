#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import RPi.GPIO as GPIO

import thsensor
import cputemp
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ =="__main__":
    threads = []
    while 1:
        try:
            # 创建新线程
            thread1 = thsensor.myThreadth(1, 17, 20,"客厅")#温湿度1
            thread2 = thsensor.myThreadth(2, 27, 20,"儿童房")#温湿度2
            #threadcpu = threading.Thread(target=cputemp.getCpuTempInterval)#cpu
            threadcpu = cputemp.myThreadth(10,"儿童房")
            # 开启新线程
            thread1.start()
            thread2.start()
            threadcpu.start()
            # 添加线程到线程列表
            threads.append(thread1)
            threads.append(thread2)
            threads.append(threadcpu)
            print threading.enumerate()
            # 等待所有线程完成
            for t in threads:
                t.join()
            print "Exiting Main Thread"
        except Exception, e:
            print e
            GPIO.cleanup()