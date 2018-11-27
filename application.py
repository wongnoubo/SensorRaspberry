#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import RPi.GPIO as GPIO

import beep
import thsensor
import cputemp

if __name__ =="__main__":
    threads = []
    while 1:
        try:
            # 创建新线程
            thread1 = thsensor.myThreadth(1, 17, 20,"thtable1")
            thread2 = thsensor.myThreadth(2, 27, 20,"thtable2")
            threadcpu = threading.Thread(target=cputemp.getCpuTempInterval)
            threadhcsr = threading.Thread(target=beep.hcsrInterval)
            # 开启新线程
            thread1.start()
            thread2.start()
            threadcpu.start()
            threadhcsr.start()
            # 添加线程到线程列表
            threads.append(thread1)
            threads.append(thread2)
            threads.append(threadcpu)
            threads.append(threadhcsr)
            print threading.enumerate()
            # 等待所有线程完成
            for t in threads:
                t.join()
            print "Exiting Main Thread"
        except Exception, e:
            print e
            GPIO.cleanup()