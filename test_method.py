# _*_coding:utf-8_*_

import urllib2, urlparse
from pywebfuzz import utils, fuzzdb
from ghost import Ghost, TimeoutError

from tag import *  # 自定义标签类

page_timeout = 60
alert_timeout = 3
xss_rsnake = ["math", "computer"]

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
            
    