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


class Mywindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableWidget.setRowCount(10)
        self.current_page = 1

        # 设置槽函数
        self.pushButton.clicked.connect(self.charu)
        self.pushButton.clicked.connect(partial(self.showdb, 0))
        self.pushButton_8.clicked.connect(self.deletedb)
        self.pushButton_2.clicked.connect(self.update)
        self.pushButton_3.clicked.connect(partial(self.showdb, 0))  # 首页
        self.pushButton_4.clicked.connect(self.prepage)  # 上一页
        self.pushButton_5.clicked.connect(self.nextpage)  # 下一页
        self.pushButton_6.clicked.connect(partial(self.tbnum, 1))  # 尾页
        self.pushButton_7.clicked.connect(self.gotopage)  # 跳转页数

        # 链接sqlite数据库
        self.database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.database.setDatabaseName('test.db')  # 如果没有该文件则自动创建
        self.database.open()
        if self.database.open():
            print('连接数据库成功')
        else:
            print(self.database.lastError().text())  # 打印操作数据库时出现的错误
        # self.table()
        self.showdb(0)
        self.tbnum(0)

    # 下一页
    def nextpage(self):
        n = (self.current_page) * 10

        if self.current_page > (self.total_page - 1):
            Msg = Message()
            Msg.msg2('已经最后一页了')
            return

        self.showdb(n)
        self.current_page = self.current_page + 1
        self.label_8.setText(str(self.current_page))

    # 上一页
    def prepage(self):
        n = (self.current_page - 2) * 10
        if self.current_page < 2:
            Msg = Message()
            Msg.msg2('已经是第一页了')
            return
        self.showdb(n)
        if n == 0:
            self.current_page = 1
            self.label_8.setText(str(self.current_page))
        else:
            self.current_page = self.current_page - 1
            self.label_8.setText(str(self.current_page))

    # 跳转指定页数
    def gotopage(self):
        the_page = int(self.lineEdit_3.text())  # 获取页数
        the_n = (the_page - 1) * 10
        if the_page <= 0 or the_page > self.total_page:
            # 如果输入的数值超出范围，提示错误
            Msg = Message()
            Msg.msg2('输入的数值超出了范围,请重新输入')
        else:
            self.showdb(the_n)
            self.label_8.setText(self.lineEdit_3.text())
            self.current_page = the_page

    # 表格获取总条目 页数
    def tbnum(self, x):
        # 获取总条目
        query = QSqlQuery()
        if query.exec('select * from zmister ORDER BY ID DESC'):
            id_index = query.record().indexOf('ID')
            db_list = []
            while query.next():
                id = query.value(id_index)
                db_list.append((id))


        # print('总条目：'+ str(len(db_list)))
        self.total_page = math.ceil(len(db_list) / 10)
        self.label_5.setText('共' + str(self.total_page) + '页')
        if x == 1:  # 点击尾页显示的数据
            n = int(self.total_page - 1) * 10
            self.showdb(n)
            self.label_8.setText(str(self.total_page))
            self.current_page = self.total_page

    # 可自定义表格
    def table(self):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(2)
        j = 0  # 第几行（从0开始）
        i = 0  # 第几列（从0开始）
        Value = "test"  # 内容
        self.tableWidget.setItem(j, i, QTableWidgetItem(Value))  # 设置j行i列的内容为Value
        self.tableWidget.setColumnWidth(j, 80)  # 设置j列的宽度
        self.tableWidget.setRowHeight(i, 50)  # 设置i行的高度
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.tableWidget.horizontalHeader().setVisible(False)  # 隐藏水平表头

    # 表格刷新数据
    def renewtb(self):
        self.showdb()

    # 数据展示在表格上
    def showdb(self, n=1):
        query = QSqlQuery()
        if query.exec('select * from zmister ORDER BY ID DESC limit {},10'.format(str(n))):
            fid_index = query.record().indexOf('fid')
            ID_index = query.record().indexOf('ID')
            weibo_index = query.record().indexOf('weibo')
            age_index = query.record().indexOf('weixin')
            pay_index = query.record().indexOf('pay')
            nr_index = query.record().indexOf('nr')
            db = []
            print("ID:",query.value(ID_index))
            while query.next():
                fid = query.value(fid_index)
                weibo = query.value(weibo_index)
                weixin = query.value(age_index)
                pay = query.value(pay_index)
                nr = query.value(nr_index)
                # print(id,weibo,weixin,pay,nr)
                db.append((fid, weibo, weixin, pay, nr))
        self.tableWidget.clearContents()  # 清除所有数据--不包括标题头
        if n == 0:
            self.label_8.setText('1')
            self.current_page = 1
        else:
            self.label_8.setText(str(self.current_page))

        self.tbnum(0)
        for i in range(len(db)):  # i是行数
            # print(db[i])
            # print(db[i][0])
            self.tableWidget.setItem(i, 1, QTableWidgetItem(db[i][0]))
            self.tableWidget.setItem(i, 2 ,QTableWidgetItem(db[i][1]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(db[i][2]))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(db[i][3]))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(db[i][4]))
            # self.tableWidget.setItem(i, 5, QTableWidgetItem(db[i][5]))  # 设置j行i列的内容为Value

    # 查询数据
    def chaxundb(self):
        query = QSqlQuery()
        if query.exec('select * from zmister'):
            id_index = query.record().indexOf('ID')
            fid_index = query.record().indexOf('fid')
            weibo_index = query.record().indexOf('weibo')
            weixin_index = query.record().indexOf('weixin')
            pay_index = query.record().indexOf('pay')
            nr_index = query.record().indexOf('nr')
            db = []
            while query.next():
                id = query.value(id_index)
                fid = query.value(fid_index)
                weibo = query.value(weibo_index)
                weixin = query.value(weixin_index)
                pay = query.value(pay_index)
                nr = query.value(nr_index)
                # print(id,weibo,weixin,pay,nr)
                db.append((id,fid, weibo, weixin, pay, nr))
            print(db)

            # 插入数据

    def charu(self):
        query = QSqlQuery()
        the_ID = self.lineEdit_4.text()  # 获取姓名
        the_weibo = self.lineEdit.text()  # 获取姓名
        the_weixin = self.lineEdit_2.text()  # 获取年龄
        the_input = self.textEdit.toPlainText()  # 获取内容框的值
        if self.radioButton.isChecked() == True:  # 判断性别
            the_pay = "是"
        else:
            the_pay = "否"

        print(the_pay)
        sql_code = 'INSERT INTO zmister (fid,weibo,weixin,pay,nr) VALUES ("{}","{}","{}","{}","{}")'.format(the_ID,the_weibo, the_weixin,
                                                                                              the_pay, the_input)
        if query.exec_(sql_code):
            print('succeed insert data')
            print()
            Msg = Message()
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.textEdit.setText('')
            self.lineEdit_4.setText('')
            Msg.msg2('添加成功')
            # 删除数据
        else:
            print("添加失败")

    def deletedb(self):
        query = QSqlQuery()
        currentRow=self.tableWidget.currentRow()
        print(currentRow)
        fid=self.tableWidget.item(currentRow,1).text()
        print(fid)
        sql_code = f'DELETE FROM zmister WHERE fid = {fid}'
        if query.exec_(sql_code):
            self.showdb(int(self.current_page-1)*10)
            print('Delete data Success')

        else:
            print('something wrong')
    # 更新数据
    def update(self):
        query = QSqlQuery()
        sql_code = f'DELETE FROM zmister WHERE ALL'
        if query.exec_(sql_code):
            print('succeed update data')


# 提示信息
# 这里是消息提示弹出框的主要代码
class Message(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 消息提示框

    def msg(self):
        QMessageBox.information(self, "提示框", "复制成功")


    def msg2(self, word):
        QMessageBox.warning(self, "提示框", word)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Mywindow()
    MainWindow.show()
    sys.exit(app.exec_())

