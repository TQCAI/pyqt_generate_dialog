# -*- coding: utf-8 -*-

import sys,os
from PyQt5.QtWidgets import *#QMessageBox,QFileDialog,QWidget,QApplication,QMainWindow,QSizePolicy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#------------------------------tools------------------------------------------------------------
import numpy as np

#------------------------------my project------------------------------------------------------------
from MainWindow import *
from Dialog import *
from SubWindow import *

useTrayIcon=False
# useTrayIcon=True

class MySubWindow(QMainWindow,Ui_SubWindow):
    '''

    '''
    def __init__(self, parent=None):
        super(MySubWindow, self).__init__(parent)
        self.setupUi(self)

    def view(self):
        if self.isVisible(): return
        self.show()

    def closeEvent(self, QCloseEvent):
        self.hide()
        QCloseEvent.ignore()

class MyDialog(QDialog):
    '''根据meta中函数的参数，生成界面'''
    def __init__(self, parent=None):
        data=[('param1', 'int'), ('param2', 'float'), ('param3', 'str'), ('param4', ['cv2.THRESH_BINARY_INV', 'cv2.THRESH_BINARY'])]
        super(MyDialog, self).__init__(parent)
        vlayout=QVBoxLayout()
        for item in data:
            label=QLabel(item[0]+':')
            param_type=item[1]
            if param_type =='float':
                widget = QDoubleSpinBox()
            elif param_type=='str':
                widget = QLineEdit()
            elif isinstance(param_type,list):
                widget=QComboBox()
                widget.addItems(param_type)
            else:
                widget=QSpinBox()
            hlayout = QHBoxLayout()
            hlayout.addWidget(label)
            hlayout.addWidget(widget)
            frame=QFrame()
            frame.setLayout(hlayout)
            vlayout.addWidget(frame)

        self.setLayout(vlayout)

    def closeEvent(self, QCloseEvent):
        self.hide()
        QCloseEvent.ignore()

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.showMenu()
        self.other()

    def iconClied(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            pw = self.parent()
            if pw.isVisible():
                pw.hide()
            else:
                pw.show()
        # self.showM('消息')

    def mClied(self):
        pass

    def showM(self,msg):
        self.showMessage("提示", msg, self.icon)

    def showMenu(self):
        self.menu = QMenu()
        self.quitAction = QAction("退出", self, triggered=self.quit)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

    def other(self):
        self.activated.connect(self.iconClied)
        #把鼠标点击图标的信号和槽连接
        self.messageClicked.connect(self.mClied)
        #把鼠标点击弹出消息的信号和槽连接
        self.setIcon(QIcon("res/python.ico"))
        self.icon = self.MessageIcon()
        #设置图标

    def quit(self):
        "保险起见，为了完整的退出"
        self.setVisible(False)
        # self.parent().exit()
        qApp.quit()
        sys.exit()

class MyMainWindow(QMainWindow, Ui_MainWindow):
    icon_trigger = pyqtSignal(str)

    def create_connection(self):
        self.button_1.clicked.connect(self.open_model_dialog)
        pass

    def init_data(self):
        self.setWindowIcon(QIcon('./res/python.png'))
        self.createRightMenu()
        # 初始化托盘程序
        if useTrayIcon:
            ti = TrayIcon(self)
            self.icon_trigger.connect(ti.showM)
            ti.show()
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool | Qt.Popup)

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.create_connection()
        self.init_data()

    def open_model_dialog(self):
        dialog=MyDialog()
        isOk=dialog.exec()

    def createRightMenu(self):
        self.rightMenu = QMenu()
        act=QAction(u'退出', self)
        self.rightMenu.addAction(act)
        self.rightMenu.triggered[QAction].connect(self.process_right_menu)

    def process_right_menu(self,q):
        text = q.text()
        if text=='退出':
            self.close()
    #关闭
    def closeEvent(self, event):
        if useTrayIcon:
            reply = QMessageBox.question(self,
                                               '本程序',
                                               "是否最小化到托盘?",
                                               QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QMessageBox.Yes)
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.accept()
                sys.exit()
            pass
        else:
            reply = QMessageBox.question(self,
                                               '本程序',
                                                "是否要退出程序？",
                                               QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QMessageBox.Yes)
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
            pass

    #绘图
    def paintEvent(self, event):
        pass
        # qp=QPainter()
        # qp.begin(self)
        # qp.setPen(QPen(Qt.red))
        # qp.setBrush(QBrush(Qt.red,Qt.SolidPattern))
        # qp.drawEllipse(x-d/2, y-d/2, d, d)
        # self.update()
        # qp.end()

    # 鼠标按下
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pass
        if event.button() == QtCore.Qt.RightButton:
            self.rightMenu.exec(QCursor.pos())

    # 鼠标释放
    def mouseReleaseEvent(self, event):
        pass

    # 鼠标移动
    def mouseMoveEvent(self, event):  # 鼠标移动
        x = event.pos().x()
        y = event.pos().y()
        # self.update()

    # 鼠标滚轮
    def wheelEvent(self, event):
        delta = event.angleDelta().y()

    #鼠标双击
    def mouseDoubleClickEvent(self, event):  # 双击
        pass

    # 键盘按下
    def keyPressEvent(self, event):
        key = ""
        if event.key() == Qt.Key_Z:
            if event.modifiers() & Qt.ControlModifier:
                key = 'ctrl+z'
        self.update()

    def img2pixmap(self, image):
        Y, X = image.shape[:2]
        self._bgra = np.zeros((Y, X, 4), dtype=np.uint8, order='C')
        self._bgra[..., 0] = image[..., 2]
        self._bgra[..., 1] = image[..., 1]
        self._bgra[..., 2] = image[..., 0]
        qimage = QtGui.QImage(self._bgra.data, X, Y, QtGui.QImage.Format_RGB32)
        pixmap = QtGui.QPixmap.fromImage(qimage)
        return pixmap

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    subWin=MySubWindow()
    myWin.button_2.clicked.connect(subWin.view)
    myWin.show()
    sys.exit(app.exec_())