#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
#温湿度转变为json文件存储到数据库中
def THresultToJson(temperature,humidity):
    data = dict(Temperature=temperature,Humidity=humidity)
    jsondata = json.dumps(data)
    print jsondata
    return jsondata

def cpuTempToJson(cputemp):
    data = dict(Cputemp = cputemp)
    jsondata = json.dumps(data)
    print jsondata
    return jsondata
