# _*_coding:utf-8_*_
reload(__import__('sys')).setdefaultencoding('utf-8')

import sys
from crawler import Crawler
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
        self.setRowCount(73)
        self.setAlternatingRowColors(True)
        self.setColumnWidth(0, 30)
        self.horizontalHeader().setStretchLastSection(True)
        self.xss_rsnake = xss_vectors  # fuzzdb.attack_payloads.xss.xss_rsnake
        for i, xss in enumerate(self.xss_rsnake):
            cb = QTableWidgetItem()
            cb.setCheckState(Qt.Checked)
            self.setItem(i, 0, cb)
            self.setItem(i, 1, QTableWidgetItem(xss))


class CookieTable(QWidget):
    def __init__(self, parent=None):
        super(CookieTable, self).__init__(parent)
        self.setWindowTitle("Cookies")
        self.resize(300, 200)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Test')
        self.initMenu()
        self.initUI()
        self.c = None

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
        self.cookie_table = CookieTable()
        cookie = QAction(QIcon(), '&Cookie', self)
        cookie.triggered.connect(self.cookie_table.show)
        self.setmenu.addAction(cookie)
        self.vector_table = VectorTable()
        vector = QAction(QIcon('vector.png'), '&Vector', self)
        vector.triggered.connect(self.vector_table.show)
        self.setmenu.addAction(vector)

    def initUI(self):
        mainwidget = QWidget()
        layout = QVBoxLayout()
        line = [QHBoxLayout() for i in range(3)]
        for l in line:
            l.setSpacing(20)
            layout.addLayout(l)
        # Line 1
        self.url_text = QLineEdit()
        self.url_text.setText(sites[0])
        line[0].addWidget(self.url_text)
        self.go_button = QPushButton("Go")
        self.connect(self.go_button, SIGNAL("clicked()"), self.go)
        line[0].addWidget(self.go_button)
        # Line 2
        line[1].addWidget(QLabel('Set-up time:'))
        self.time_text = QLineEdit()
        line[1].addWidget(self.time_text)
        line[1].addWidget(QLabel('Cookie:'))
        self.cookie_text = QLineEdit()
        # self.cookie_text.setText('cookies.txt')
        line[1].addWidget(self.cookie_text)
        open_button = QPushButton("Open")
        line[1].addWidget(open_button)
        line[1].addSpacing(95)
        # Line 3
        self.initTabWidget()
        line[2].addWidget(self.tabwidget)
        mainwidget.setLayout(layout)
        self.setCentralWidget(mainwidget)

    def initTabWidget(self):
        self.tabwidget = QTabWidget()
        console_tab = QSplitter(Qt.Horizontal, self)
        self.crawler_tab = QTextBrowser(self)
        self.console_split = QTextBrowser(console_tab)
        self.xss_split = QTextBrowser(console_tab)
        console_tab.setStretchFactor(0, 1)
        for b in [self.console_split, self.xss_split, self.crawler_tab]:
            b.setWordWrapMode(QTextOption.NoWrap)
        self.tabwidget.addTab(self.crawler_tab, 'Url')
        self.tabwidget.addTab(console_tab, 'Console')

    def closeEvent(self, event):
        if self.c:
            self.c.exit()
        sys.exit()

    def display(self, content, format=None, widget=None):
        content = self.tr(content)
        if widget == 'xss':
            w = self.xss_split
        elif widget == 'url':
            w = self.crawler_tab
        else:
            w = self.console_split
        if format:
            content = format.replace('$', content)
            w.moveCursor(QTextCursor.End)
            w.append(content)
        else:
            w.append('')
            w.moveCursor(QTextCursor.End)
            w.insertPlainText(content)
            # vb = w.verticalScrollBar()
            # vb.setValue(vb.maximum())

    def go(self):
        self.go_button.setEnabled(False)
        for b in [self.crawler_tab, self.console_split, self.xss_split]:
            b.clear()
        url = unicode(self.url_text.text(), encoding="utf-8")
        set_up = unicode(self.time_text.text(), encoding="utf-8")
        cookie_file = unicode(self.cookie_text.text(), encoding="utf-8")
        try:
            set_up = int(set_up)
        except ValueError:
            set_up = 0
        self.c = Crawler(url, set_up, str(cookie_file), self)
        self.c.go()  # go_button.setEnabled(True)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec_()
