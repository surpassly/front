# _*_coding:utf-8_*_
import sys

reload(__import__('sys')).setdefaultencoding('utf-8')
from pywebfuzz import fuzzdb
from test import Test
from sites import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class VectorTable(QTableWidget):
    def __init__(self, parent=None):
        super(VectorTable, self).__init__(parent)
        self.setWindowTitle("xss_snake")
        self.resize(300, 600)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["", "XSS Payloads"])
        self.setRowCount(80)
        self.setAlternatingRowColors(True)
        self.setColumnWidth(0, 30)
        self.horizontalHeader().setStretchLastSection(True)
        self.xss_rsnake = ['math'] + fuzzdb.attack_payloads.xss.xss_rsnake[:]
        for i, xss in enumerate(self.xss_rsnake):
            cb = QTableWidgetItem()
            cb.setCheckState(Qt.Checked)
            self.setItem(i, 0, cb)
            self.setItem(i, 1, QTableWidgetItem(xss))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Test')
        self.initMenu()
        self.initUI()

    def closeEvent(self, event):
        sys.exit()

    def display(self, content, format=None, widget=None):
        content = self.tr(content)
        if widget == 'xss':
            content = content.replace("<", "&lt;").replace(">", "&gt;")
            if format:
                content = format.replace('$', content)
            self.tabwidget.setCurrentIndex(0)
            self.xss_split.append(content)
        else:
            if format:
                content = format.replace('$', content)
            self.tabwidget.setCurrentIndex(0)
            self.console_split.append(content)

    def initMenu(self):
        menubar = self.menuBar()
        # File
        self.filemenu = menubar.addMenu('&File')
        exit = QAction(QIcon('exit.png'), '&Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.triggered.connect(sys.exit)
        self.filemenu.addAction(exit)
        # Setting
        self.setmenu = menubar.addMenu('&Settings')
        self.vector_table = VectorTable()
        vector = QAction(QIcon('vector.png'), '&Vector', self)
        vector.triggered.connect(self.vector_table.show)
        self.setmenu.addAction(vector)

    def initUI(self):
        mainwidget = QWidget()
        grid = QGridLayout()
        grid.setSpacing(10)
        self.urlText = QLineEdit()
        self.urlText.setText(sites[0])
        grid.addWidget(self.urlText, 0, 0)
        self.go_button = QPushButton("Go")
        self.connect(self.go_button, SIGNAL("clicked()"), self.goTest)
        grid.addWidget(self.go_button, 0, 1)
        self.initTabWidget()
        grid.addWidget(self.tabwidget, 1, 0, 1, 2)
        mainwidget.setLayout(grid)
        self.setCentralWidget(mainwidget)

    def initTabWidget(self):
        self.tabwidget = QTabWidget()
        console_tab = QSplitter(Qt.Horizontal, self)
        self.console_split = QTextBrowser(console_tab)
        self.xss_split = QTextBrowser(console_tab)
        console_tab.setStretchFactor(0, 1)
        for b in [self.console_split, self.xss_split]:
            b.setWordWrapMode(QTextOption.NoWrap)
        self.tabwidget.addTab(console_tab, 'Console')

    def goTest(self):
        self.go_button.setDisabled(True)
        for b in [self.console_split, self.xss_split]:
            b.clear()
        url = unicode(self.urlText.text(), encoding="utf-8")
        t = Test(url, self)  # self.go_button.setDisabled(False)
        # setVector
        t.go()
        del t
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec_()
