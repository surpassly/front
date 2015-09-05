# _*_coding:utf-8_*_

import urlparse
from posixpath import normpath
from ghost import Ghost, TimeoutError
from test import Test
from bs4 import BeautifulSoup

page_timeout = 30
alert_timeout = 3


def dvwa_security(ghost, level):
    ghost.open('http://127.0.0.1/dvwa/')
    ghost.fill("form", {"username": 'admin', "password": 'password'})
    ghost.click('input[type=submit]', expect_loading=True)
    ghost.open('http://127.0.0.1/dvwa/security.php')
    ghost.evaluate("document.getElementsByName('security')[0].value = '%s';" % level)
    ghost.click('input[type=submit]', expect_loading=True)


def slash(url):
    if not url.endswith('/'):
        url += '/'
    return url


class Crawler:
    def __init__(self,
                 location,
                 setup_timeout=0,
                 cookie_file=None,
                 mainwindow=None):
        self.mainwindow = mainwindow
        self.__ghost = Ghost().start()
        self.__ghost.wait_timeout = page_timeout
        self.__ghost.download_images = False
        if cookie_file != '':
            try:
                self.__ghost.load_cookies(cookie_file)
            except IOError:
                self.display("cookie: IOError", '<font color=red>$</font>', 'url')
        if setup_timeout != 0:
            self.__ghost.show()
        self.setup_timeout = setup_timeout
        self.max_depth = 1
        self.url_queue = []
        self.location = location
        # dvwa_security(self.__ghost, 'low')

    def display(self, content, format=None, widget=None):
        print content
        if self.mainwindow:
            self.mainwindow.display(content, format, widget)

    def convert_a(self, location, a):
        if str(type(a)) == "<class 'bs4.element.Tag'>":
            try:
                href = a['href']
            except KeyError:
                return None
        elif str(type(a)) == "<type 'str'>":
            href = a
        else:
            return None  # <type 'unicode'>
        href = href.strip()
        # useless
        if href.lower() in ['javascript:;', "javacript:void(0);", "javascript:void(0)", "javascript:void(0);",
                           'return false;', '/', "http://www", ""]:
            return None
        for s in ['mailto:', '#', 'javascript:']:
            if href.lower().startswith(s):
                return None
        # normal
        if href.startswith('http://') or href.startswith('https://'):
            return href
        # path
        if href.startswith("//"):
            href = "http:" + href  # //www.baidu.com/s
        elif href.startswith("/"):
            href = self.host + href[1:]
        else:
            href = slash(location) + href
        return href

    def crawler_page(self, location, depth):
        if depth >= self.max_depth:
            return
        try:
            self.__ghost.open(location)
            current_url, resources = self.__ghost.evaluate('window.location.href')  # redirect
            location = str(current_url)
        except TimeoutError:
            return
        urls = []
        soup = BeautifulSoup(str(self.__ghost.content), from_encoding='utf-8')
        bs_as = soup.find_all('a')
        for a in bs_as:
            url = self.convert_a(location, a)
            if url:
                r = urlparse.urlparse(url)
                host = slash(r.scheme + "://" + r.netloc)
                if host == self.host and url not in self.url_queue:
                    self.display(url,  "<a href='$'>$<a>", 'url')
                    self.url_queue.append(url)
                    urls.append(url)
        for url in urls:
            self.crawler_page(url, depth + 1)

    def go(self):
        self.display("...crawling", "<b>$<b>", 'url')
        try:
            self.__ghost.open(self.location)
            current_url, resources = self.__ghost.evaluate('window.location.href')  # redirect
            self.location = str(current_url)
            r = urlparse.urlparse(self.location)
            self.host = slash(r.scheme + "://" + r.netloc)  # redirect
            self.display(self.location,  "<a href='$'>$<a>", 'url')
            self.url_queue.append(self.location)
        except TimeoutError:
            self.display("init: TimeoutError", '<font color=red>$</font>', 'url')
            self.exit()
            return
        self.__ghost.sleep(self.setup_timeout)
        self.crawler_page(self.location, 0)  # url, depth
        # Test
        for url in self.url_queue:
            t = Test(self.__ghost, url, self.mainwindow)
            t.test()
        self.exit()

    def exit(self):
        self.display("finish", "<b>$<b>", 'url')
        self.__ghost.hide()
        if self.mainwindow:
            self.mainwindow.go_button.setEnabled(True)
        self.__ghost.sleep(120)
        # self.__ghost.exit()


if __name__ == '__main__':
    reload(__import__('sys')).setdefaultencoding('utf-8')
    location = 'http://www.baidu.com'
    c = Crawler(location)
    c.go()

