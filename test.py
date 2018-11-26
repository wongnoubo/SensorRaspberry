#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb

def mysqlDbthvalue(tablename):
    # 建立和数据库的连接
    db = MySQLdb.connect(host='119.23.248.55', user="root", passwd="123456", db="sensor")
    # 获取操作游标
    cursor = db.cursor()
    createtablesql="CREATE TABLE if not exists "+tablename +" ( `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, `thvalue` varchar(50) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cursor.execute(createtablesql)
    cursor.close()
    db.commit()
    db.close()

if __name__ =="__main__":
    mysqlDbthvalue("thvalue1")
