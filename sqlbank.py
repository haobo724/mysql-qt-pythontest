import os, time, datetime, sys, random, math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from Ui_info5 import Ui_MainWindow
from functools import partial
# 导入数据库
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery

def create_db():
    try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('test.db')

            if db.open():
                print('连接数据库成功')
            else:
                print(db.lastError().text()) # 打印操作数据库时出现的错误

            # 实例化一个查询对象
            query = QtSql.QSqlQuery()
            # 创建一个数据库表，返回一个布尔值
            query.exec_("create table zmister(ID int primary key,"
                        "fid varchar(20), weibo varchar(100), weixin varchar(50), pay varchar(10), nr varchar(111))")
            # 插入数据
            query.exec_("insert into zmister values(1000, 'sogou', 'https://soso.com','https://soso.com','https://soso.com','https://soso.com')")
            print('创建数据库成功')
    except Exception as e:
        print(e)


create_db()