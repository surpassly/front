# _*_coding:utf-8_*_
reload(__import__('sys')).setdefaultencoding('utf-8') 

import time, urllib2, urlparse
from ghost import Ghost, TimeoutError
from pywebfuzz import utils, fuzzdb
from bs4 import BeautifulSoup
from tag import *
from sites import*

page_timeout = 60
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


def get_attrs(list, soup):
    val = []
    for attr in list:
        val.append(soup[attr] if attr in soup.attrs else '')
    val.append(soup.prettify())  # outerHTML
    return val
            
    
def capture_page(ghost, url):
    name = url.replace('\\', '').replace('/', '').replace(':', '').replace('?', '').replace('&', '').replace('=', '').replace('#', '')
    ghost.capture_to(name[4:] + ".png", region=(0, 0, 600, 400))


class Test():
    def __init__(self, location, mainwindow = None):
        self.mainwindow = mainwindow
        self.addMessage("<b>%s ...opening</b>" % location)
        print "%s ...opening" % location
        self.__ghost = Ghost(wait_timeout=page_timeout, download_images=False, display=True)
        # dvwa_security(self.__ghost, "low")
        try:
            self.__ghost.open(location)
        except TimeoutError:
            return
        r = urlparse.urlparse(location)
        self.host = r.scheme + "://" + r.netloc
        self.__as = []
        self.__inputs = []
        self.__buttons = []
        self.__forms = []
        self.location = location
        soup = BeautifulSoup(str(self.__ghost.content), from_encoding='utf-8')
        self.__getInputsAndForms(soup)
        self.xss_rsnake = ["math", "computer"]  # fuzzdb.attack_payloads.xss.xss_rsnake[:2]

    def addMessage(self, content, widget=None):
        if self.mainwindow:
            self.mainwindow.addMessage(content, widget)

    def __convertAction(self, action):
        host = slash(self.host)
        action = action.strip()
        if action.startswith("http"):
            action = slash(action)
        elif action.startswith("//"):
            action = "http:" + action  # //www.baidu.com/s
        elif action.startswith("#") or action == '':
            action = slash(self.location)
        else:
            if action.startswith('/'):
                action = host + action[1:]
            else:
                action = host + action
        if action.endswith('?'):
            action = action[:-1]
        return action         
        
    def __getInputsAndForms(self, soup):
        # <a>
        bs_as = soup.find_all('a')
        for bs_a in bs_as:
            attrs = get_attrs(["href"], bs_a)
            self.__as.append(A(*attrs))
        # <input>
        bs_inputs = soup.find_all('input')
        for bs_input in bs_inputs:
            attrs = get_attrs(["id", "name", "type", "value"], bs_input)
            self.__inputs.append(Input(*attrs))
        # <button>
        bs_buttons = soup.find_all('button')
        for bs_button in bs_buttons:
            attrs = get_attrs(["class", "id", "name", "type"], bs_button)
            self.__buttons.append(Button(*attrs))
        # <form>
        bs_forms = soup.find_all('form')
        for bs_form in bs_forms:
            form_as = []
            bs_as = soup.find_all('a')
            for bs_a in bs_as:
                attrs = get_attrs(["href"], bs_a)
                form_as.append(A(*attrs))
            form_inputs = []
            bs_inputs = bs_form.find_all('input')
            for bs_input in bs_inputs:
                attrs = get_attrs(["id", "name", "type", "value"], bs_input)
                form_inputs.append(Input(*attrs))
            form_buttons = []
            for bs_button in bs_buttons:
                attrs = get_attrs(["class", "id", "name", "type"], bs_button)
                form_buttons.append(Button(*attrs))
            attrs = get_attrs(["action", "id", "method", "name"], bs_form)
            attrs.append(form_as)
            attrs.append(form_inputs)
            attrs.append(form_buttons)
            self.__forms.append(Form(*attrs))

        for form in self.__forms:
            for a in form.as_:
                for i in self.__as:
                    if a.outerHTML == i.outerHTML:
                        self.__as.remove(i)
            for input in form.inputs:
                for i in self.__inputs:
                    if input.outerHTML == i.outerHTML:
                        self.__inputs.remove(i)
            for button in form.buttons:
                for i in self.__buttons:
                    if button.outerHTML == i.outerHTML:
                        self.__buttons.remove(i)
            self.addMessage(str(form), 'form')        
        for a in self.__as:
            self.addMessage(str(a), 'a')
        for input in self.__inputs:
            self.addMessage(str(input), 'input')
        for button in self.__buttons:
            self.addMessage(str(button), 'button')
        return
            
    def testFormsWithGhost(self):        
        for i, form in enumerate(self.__forms): 
            # doc, res = self.__ghost.evaluate("document.querySelectorAll('form')[%d].parentNode.outerHTML;" % i)
            # print doc
            self.addMessage(str(form))
            print form
            for xss in self.xss_rsnake:
                try:
                    self.__ghost.open(self.location)
                    self.__ghost.evaluate('''
                    var form = document.querySelectorAll('form')[%d];
                    var tagElements = form.parentNode.getElementsByTagName('input');
                    for (var i = 0; i < tagElements.length; i++){                      
                        var input = tagElements[i]
                        if (input.type == "" || input.type == "text" || input.type == "password" || (input.type == "hidden" && input.value == "")) {
                            input.removeAttribute('onfocus');
                            input.value = '%s';
                        }
                    }
                    form.target = '_self';
                    form['submit']();''' % (i, xss), expect_loading=True)   
                    # self.__ghost.click("input[type=submit]", expect_loading=True)
                    # self.__ghost.click('button[class=doSearch]', expect_loading=True)
                    # self.__ghost.click("a[class='search_btn search_btn_enter_ba j_enter_ba']", expect_loading=True)
                    try:
                        result, resources = self.__ghost.wait_for_alert(timeout=alert_timeout)
                        self.addMessage('<b>alert: %s</b>' % result)
                        print 'alert: %s' % result
                        if result == 'XSS':
                            break
                    except TimeoutError:
                        pass
                    finally:
                        url, resources = self.__ghost.evaluate('window.location.href')
                        self.addMessage("<a href='%s'>%s</a>" % (url, url))
                        print url
                        # capture_page(self.__ghost, url)
                except TimeoutError:
                    print "testFormsWithGhost: TimeoutError"
        # exit
        if self.mainwindow:
            self.mainwindow.go_button.setDisabled(False)
        self.__ghost.hide()
        self.__ghost.sleep(60)
        return
    
    def testForm(self, form):
        print form
        if form.method == "post":
            print "post: pass"
            return
        for xss in self.xss_rsnake:
            postdata = ''
            for i in form.inputs:
                if i.name != '':
                    if i.type in ["", "text", "password"] or i.value == '':
                        postdata += '%s=%s&' % (i.name, urllib2.quote(xss))
                    elif i.type == 'hidden' and i.value != '':
                        postdata += '%s=%s&' % (i.name, i.value)  # hidden
            location = self.__convertAction(form.action) + '?' + postdata   
            print location
            try:
                self.__ghost.open(location)
            except TimeoutError:
                print "test_method: TimeoutError"
            try:
                result, resources = self.__ghost.wait_for_alert(timeout=alert_timeout)
                print 'alert:', result
                if result == 'XSS':
                    break
            except TimeoutError:
                pass
        return
    
    def __str__(self):
        r = ""
        for input in self.__inputs:
            r += str(input) + '\n' 
        for form in self.__forms:
            r += str(form) + '\n'
        return r if r != "" else "InitError"

    def __del__(self):
        # self.__ghost.exit()
        return


if __name__ == '__main__':
    start = time.clock()
    for location in sites:
        t = Test(location)
        t.testFormsWithGhost()
    end = time.clock()
    print 'time:', end - start
