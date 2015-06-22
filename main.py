# _*_coding:utf-8_*_
reload(__import__('sys')).setdefaultencoding('utf-8') 

import time
from pywebfuzz import utils, fuzzdb
from bs4 import BeautifulSoup

from tag import *  # 自定义标签类
from test import *  # 自定义测试类
from sites import *

page_timeout = 60
alert_timeout = 3

#location = "http://www.baidu.com/"

start = time.clock()

'''
host = "www.vanishingincmagic.com"
doc = utils.make_request("http://www.vanishingincmagic.com/")
soup = BeautifulSoup(doc[1], from_encoding='utf-8') #以防编码问题
'''

ghost = Ghost(wait_timeout=page_timeout, download_images=False, display=True)

sites = ["http://v.baidu.com"]

for location in sites:
    print location
    try:
        ghost.open(location)
    except TimeoutError:
        print "TimeoutError"
    
    soup = BeautifulSoup(str(ghost.content), from_encoding='utf-8')  # 以防编码问题
    
    inputs = []
    bs_inputs = soup.find_all('input')
    for bs_input in bs_inputs:    
        id = bs_input['id'] if 'id' in bs_input.attrs else ''
        name = bs_input['name'] if 'name' in bs_input.attrs else ''
        type = bs_input['type'] if 'type' in bs_input.attrs else ''
        value = bs_input['value'] if 'value' in bs_input.attrs else ''
        inputs.append(Input(id, name, type, value))
        
    forms = []
    bs_forms = soup.find_all('form')
    for bs_form in bs_forms:    
        form_inputs = []
        bs_inputs = bs_form.find_all('input')
        for bs_input in bs_inputs:
            id = bs_input['id'] if 'id' in bs_input.attrs else ''
            name = bs_input['name'] if 'name' in bs_input.attrs else ''
            type = bs_input['type'] if 'type' in bs_input.attrs else ''
            value = bs_input['value'] if 'value' in bs_input.attrs else ''
            form_inputs.append(Input(id, name, type, value))
        action = bs_form['action'] if 'action' in bs_form.attrs else ''
        id = bs_form['id'] if 'id' in bs_form.attrs else ''
        method = bs_form['method'] if 'method' in bs_form.attrs else ''
        name = bs_form['name']  if 'name' in bs_form.attrs else ''
        forms.append(Form(action, id, method, name, form_inputs))
        
    # 删除重复inputs
    for form in forms:
        for input in form.inputs:
            for i in inputs:
                if (input.id, input.name, input.type) == (i.id, i.name, i.type):
                    inputs.remove(i)
    
    for input in inputs:
        print input 
    for form in forms:
        print form
        test_form_ghost(ghost, location, form)
            
    end = time.clock()
    print 'time:', end - start