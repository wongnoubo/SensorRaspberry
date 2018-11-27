#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import camera
import threading

BEEPPORT = 4  # GPIO7
HCSRPORT = 18  # GPIO12

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(HCSRPORT, GPIO.IN)
    GPIO.setup(BEEPPORT, GPIO.OUT)

def beep():
    for i in range(1, 3):
        GPIO.output(BEEPPORT, GPIO.LOW)  # 蜂鸣器低电平响
        time.sleep(0.5)
        GPIO.output(BEEPPORT, GPIO.HIGH)
        time.sleep(0.5)

def detct():
    time.sleep(1)
    personflag=0
    if GPIO.input(HCSRPORT) == True:
        print "Someone is closing!"
        camera.camera()
        beep()
        personflag = 1
        return personflag
    else:
        GPIO.output(BEEPPORT, GPIO.HIGH)
        print "No anybody!"

#10s检查一次
def hcsrInterval():
    init()
    cputempthread = threading.Timer(6,detct)
    cputempthread.start()

