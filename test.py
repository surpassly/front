# _*_coding:utf-8_*_
reload(__import__('sys')).setdefaultencoding('utf-8') 

import urllib2, urlparse
from pywebfuzz import utils, fuzzdb
from ghost import Ghost, TimeoutError

from tag import *  # 自定义标签类

page_timeout = 60
alert_timeout = 3
xss_rsnake = ["数学", "计算机", "音乐", "美术", "物理"]

def test_url(url):
    return


def test_inputs(ghost, location, inputs):  # form以外的inputs
    actions = []
    xss = "<SCRIPT>alert('XSS');</SCRIPT>"
    for input in inputs:
        if input.type in ["", "text", "password"]:
            ghost.set_field_value("*[name=%s]" % input.name, xss)
            '''focus 提交该input 进入新页面 分析url'''
            url, resources = ghost.evaluate('window.location.href')
            r = urlparse.urlparse(str(url))
            params = []
            for param in r.query.split('&'):
                params.append(param.split('=')[0])
            actions.append(Action(r.path, params))
        elif input.type in ["button", "submit"]:
            ghost.click('input[name=%s]' % input.name)  # , expect_loading=True)
            '''看返回值 分析页面变化 或进入新页面'''
            

def test_form_ghost(ghost, location, form):
    for i, xss in enumerate(xss_rsnake):
        try:
            ghost.open(location)
            for input in form.inputs:
                if input.type in ["", "text", "password"]:
                    ghost.evaluate("document.getElementsByName('%s')[0].removeAttribute('onfocus');" % input.name)
                    if input.name != '':
                        ghost.set_field_value("*[name=%s]" % input.name, xss)
                    elif input.id != '':
                        ghost.set_field_value("*[id=%s]" % input.id, xss)       
            '''
            有时需要移除onfocus属性
            提交方式有时不管用
            '''
            # 提交表单
            # ghost.click('input[type=submit]')#, expect_loading=True)
            ghost.evaluate('''
            document.getElementById('%s').target = '_self';
            document.querySelector('form[id=%s]')['submit']();''' % (form.id, form.id), expect_loading=True)       
            try:
                ghost.wait_timeout = alert_timeout
                result, resources = ghost.wait_for_alert()
                print 'alert:', result
                if result == 'XSS':
                    break
            except TimeoutError:
                pass
            finally:
                ghost.wait_timeout = page_timeout
                url, resources = ghost.evaluate('window.location.href')
                print url
        except TimeoutError:
            print "TimeoutError"
            
            
def test_form(ghost, host, location, form):
    for i, xss in enumerate(xss_rsnake):
        postdata = ''
        for i in form.inputs:
            if i.type in ['' , 'text', 'password']:
                i.value = urllib2.quote(xss)
            if i.name != '' and i.value != '':
                postdata += '%s=%s&' % (i.name, i.value)
        location = "http://" + form.host + form.action + '?' + postdata
        try:
            ghost.open(location)
        except TimeoutError:
            print "TimeoutError"
        try:
            ghost.wait_timeout = alert_timeout
            result, resources = ghost.wait_for_alert()
            print 'alert:', result
            if result == 'XSS':
                break
        except TimeoutError:
            pass
        finally:
            ghost.wait_timeout = page_timeout
            url, resources = ghost.evaluate('window.location.href')
    
