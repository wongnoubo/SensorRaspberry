#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import RPi.GPIO as GPIO

import beep

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__=="__main__":
    threads = []
    while 1:
        try:
            thread1 = beep.cameraThreadth(6)#执行的时间间隔是6s
            thread1.start()
            threads.append(thread1)
            print threading.enumerate()
            for t in threads:
                t.join()
            print "Exiting Main Thread"
        except Exception, e:
            print e
            GPIO.cleanup()