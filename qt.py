# _*_coding:utf-8_*_
import sys
reload(__import__('sys')).setdefaultencoding('utf-8') 
from test import Test
from sites import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(100, 100, 600, 480)
        self.setWindowTitle('Test')  
        self.initMenu()
        self.initUI()
        
    def addMessage(self, content, widget=None):
        if widget == 'form':
            self.tabwidget.setCurrentIndex(1)
            self.form_tab.append(content)
        elif widget == 'a':
            self.tabwidget.setCurrentIndex(2)
            self.input_tab.append(content)
        elif widget == 'input':
            self.tabwidget.setCurrentIndex(3)
            self.input_tab.append(content)
        elif widget == 'button':
            self.tabwidget.setCurrentIndex(4)
            self.button_tab.append(content)
        else:
            self.tabwidget.setCurrentIndex(0)
            self.console_tab.append(content)
        
    def initMenu(self):
        menubar = self.menuBar()
        self.filemenu = menubar.addMenu('&File')
        exit = QAction(QIcon('exit.png'), '&Exit', self)        
        exit.setShortcut('Ctrl+Q')
        exit.triggered.connect(sys.exit)
        self.filemenu.addAction(exit)

    def closeEvent(self, event):
        sys.exit()

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
        self.initTabwidget()
        grid.addWidget(self.tabwidget, 1, 0, 1, 2)
        mainwidget.setLayout(grid)
        self.setCentralWidget(mainwidget)
    
    def initTabwidget(self):
        self.tabwidget = QTabWidget() 
        self.console_tab = QTextBrowser()
        self.a_tab = QTextBrowser()
        self.input_tab = QTextBrowser()
        self.button_tab = QTextBrowser()
        self.form_tab = QTextBrowser()
        self.tabwidget.addTab(self.console_tab, 'Console')
        self.tabwidget.addTab(self.form_tab, '<form>')
        self.tabwidget.addTab(self.a_tab, '<a>')
        self.tabwidget.addTab(self.input_tab, '<input>')
        self.tabwidget.addTab(self.button_tab, '<button>')
        
    def goTest(self):
        self.go_button.setDisabled(True)
        url = unicode(self.urlText.text(), encoding="utf-8")
        Test(url, self)
        return
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec_()
