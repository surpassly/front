# _*_coding:utf-8_*_
reload(__import__('sys')).setdefaultencoding('utf-8')

import os, time, random, string
import urlparse
from ghost import Ghost, TimeoutError
from pywebfuzz import fuzzdb
from bs4 import BeautifulSoup
from tag import *
from sites import *

page_timeout = 30
alert_timeout = 3


def baidu_login(ghost):
    ghost.open('http://www.baidu.com')
    ghost.evaluate("document.querySelector('a[name=tj_login]').click()")
    try:
        ghost.wait_for_selector("form[id=TANGRAM__PSP_8__form]")
        ghost.evaluate('''
        var form = document.querySelector('form[id=TANGRAM__PSP_8__form]');
        document.querySelector('input[id=TANGRAM__PSP_8__userName]').value = "surpassly";
        document.querySelector('input[id=TANGRAM__PSP_8__password]').value = "myself";
        document.querySelector('input[id=TANGRAM__PSP_8__submit]').click()
        form['submit']();
        ''', expect_loading=True)
        ghost.sleep(10)
    except TimeoutError:
        pass


def dvwa_security(ghost, level):
    ghost.open('http://127.0.0.1/dvwa/')
    ghost.fill("form", {"username": 'admin', "password": 'password'})
    ghost.click('input[type=submit]', expect_loading=True)
    ghost.open('http://127.0.0.1/dvwa/security.php')
    ghost.evaluate("document.getElementsByName('security')[0].value = '%s';" % level)
    ghost.click('input[type=submit]', expect_loading=True)


def create_spy():
    count = random.choice(range(5, 10))
    return ''.join(random.choice(string.letters) for i in range(count))


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


def get_as(soup):
    res = []
    bs_as = soup.find_all('a')
    for bs_a in bs_as:
        attrs = get_attrs(["class", "href"], bs_a)
        res.append(A(*attrs))
    return res


def get_inputs(soup):
    res = []
    bs_inputs = soup.find_all('input')
    for bs_input in bs_inputs:
        attrs = get_attrs(["class", "id", "name", "type", "value"], bs_input)
        res.append(Input(*attrs))
    return res


def get_buttons(soup):
    res = []
    bs_buttons = soup.find_all('button')
    for bs_button in bs_buttons:
        attrs = get_attrs(["class", "id", "name", "type"], bs_button)
        res.append(Button(*attrs))
    return res


def get_textareas(soup):
    res = []
    bs_textareas = soup.find_all('textarea')
    for bs_textarea in bs_textareas:
        attrs = get_attrs(["class", "id", "name", "value"], bs_textarea)
        res.append(TextArea(*attrs))
    return res


class Test():
    def __init__(self, location, mainwindow=None, username=None):
        self.mainwindow = mainwindow
        self.username = username
        self.__as = []
        self.__inputs = []
        self.__buttons = []
        self.__textareas = []
        self.__forms = []
        self.location = location
        self.spy = [create_spy(), create_spy()]
        self.xss_rsnake = fuzzdb.attack_payloads.xss.xss_rsnake
        self.__ghost = Ghost(wait_timeout=page_timeout, download_images=False, display=True)

    def go(self):
        self.display("%s ...opening" % self.location, '<b>$</b>')
        try:
            self.__ghost.open(self.location)
        except TimeoutError:
            self.display("init: TimeoutError", '<font color=red>$</font>')
            self.exit()
            return
        if self.username:
            try:
                self.__ghost.wait_for_text(self.username, timeout=60)
                self.__ghost.sleep(8)  # 8
            except TimeoutError:
                pass
        soup = BeautifulSoup(str(self.__ghost.content), from_encoding='utf-8')
        self.__get_all_tags(soup)
        if str(self) != "":
            self.display(str(self))
            self.display('...testing', '<b>$</b>')
            self.test_forms_ghost()
            self.test_inputs_ghost()
        else:
            self.display('get nothing', '<b>$</b>')
        self.exit()

    def display(self, content, format=None, widget=None):
        print content
        if self.mainwindow:
            self.mainwindow.display(content, format, widget)

    def __get_all_tags(self, soup):
        self.__as = get_as(soup)
        self.__inputs = get_inputs(soup)
        self.__buttons = get_buttons(soup)
        self.__textareas = get_textareas(soup)
        bs_forms = soup.find_all('form')
        for bs_form in bs_forms:
            attrs = get_attrs(["action", "id", "method", "name"], bs_form)
            for f in [get_as(bs_form), get_inputs(bs_form), get_buttons(bs_form), get_textareas(bs_form)]:
                attrs.append(f)
            self.__forms.append(Form(*attrs))
        # delete
        for form in self.__forms:
            f_list = [form.as_, form.inputs, form.buttons, form.textareas]
            s_list = [self.__as, self.__inputs, self.__buttons, self.__textareas]
            for i in range(0, len(f_list)):
                for f in f_list[i]:
                    for s in s_list[i]:
                        if f.outerHTML == s.outerHTML:
                            s_list[i].remove(s)
        return

    def test_inputs_ghost(self):
        for i, input in enumerate(self.__inputs):
            self.display(str(input))
            if input.type not in ['button', 'submit']:
                continue
            flag = 0  # spy
            for j, xss in enumerate(self.spy + self.xss_rsnake):
                self.display(xss, widget='xss')
                xss = xss.replace('"', '\\"')
                try:
                    self.__ghost.open(self.location)
                    self.__ghost.evaluate('''
                    var xss = "%s"
                    var tagElements = document.getElementsByTagName("textarea");
                    for (var i = 0; i < tagElements.length; i++) {
                        var text = tagElements[i];
                        text.innerHTML = xss
                    };
                    tagElements = document.getElementsByTagName("input");
                    for (var i = 0; i < tagElements.length; i++) {
                        var input = tagElements[i];
                        if (input.type == "" || input.type == "text" || input.type == "password" || (input.type == "hidden" && input.value == "")) {
                            input.removeAttribute("onfocus");
                            input.value = xss
                        }
                    };
                    tagElements[%d].click();
                    ''' % (xss, i), expect_loading=True)
                    # self.__ghost.click("input[class='%s']" % str(' '.join(input.class_)), expect_loading=True)
                    if j < len(self.spy) and not self.__identify_spy(xss):
                        flag += 1
                        if flag == len(self.spy):
                            break
                    self.__identify_xss()
                    self.capture_page(i, j)
                except TimeoutError:
                    self.display("test_inputs: TimeoutError", '<font color=red>$</font>', 'xss')
                    if j < len(self.spy):
                        flag += 1
                        if flag == len(self.spy):
                            break

    def test_forms_ghost(self):
        for i, form in enumerate(self.__forms):
            self.display(str(form))
            flag = 0  # spy
            for j, xss in enumerate(self.spy + self.xss_rsnake):
                self.display(xss, widget='xss')
                xss = xss.replace('"', '\\"')
                try:
                    self.__ghost.open(self.location)
                    self.__ghost.evaluate('''
                    var xss = "%s"
                    var form = document.querySelectorAll("form")[%d];
                    var tagElements = form.getElementsByTagName("textarea");
                    for (var i = 0; i < tagElements.length; i++) {
                        var text = tagElements[i];
                        text.innerHTML = xss
                    };
                    tagElements = form.getElementsByTagName("input");
                    for (var i = 0; i < tagElements.length; i++) {
                        var input = tagElements[i];
                        if (input.type == "" || input.type == "text" || input.type == "password" || (input.type == "hidden" && input.value == "")) {
                            input.removeAttribute("onfocus");
                            input.value = xss
                        }
                    }
                    form.target = "_self";
                    form["submit"]();''' % (xss, i), expect_loading=True)
                    # self.__ghost.click('button[class=doSearch]', expect_loading=True)
                    # self.__ghost.click("a[class='search_btn search_btn_enter_ba j_enter_ba']", expect_loading=True)
                    if j < len(self.spy) and not self.__identify_spy(xss):
                        flag += 1
                        if flag == len(self.spy):
                            break
                    self.__identify_xss()
                    self.capture_page(i, j)
                except TimeoutError:
                    self.display("test_forms: TimeoutError", '<font color=red>$</font>', 'xss')
                    if j < len(self.spy):
                        flag += 1
                        if flag == len(self.spy):
                            break

    def __identify_spy(self, spy):
        result = False
        try:
            result, resources = self.__ghost.wait_for_text(spy, timeout=alert_timeout)
        except TimeoutError:
            pass
        finally:
            url, resources = self.__ghost.evaluate('window.location.href')
            self.display(str(url), "<a href='$'>$<a>", 'xss')
        return result

    def __identify_xss(self):
        flag = False
        try:
            result, resources = self.__ghost.wait_for_alert(timeout=alert_timeout)
            self.display('alert: %s' % result, '<b>$</b>', 'xss')
            if result == 'XSS':
                flag = True  # identified
        except TimeoutError:
            pass
        return flag

    def capture_page(self, i, j):
        r = urlparse.urlparse(self.location)
        dir = r.netloc + r.path.replace('/', '_')
        if not os.path.exists(os.getcwd() + '\\' + dir):
            os.mkdir(dir)
        w, res = self.__ghost.evaluate('document.body.scrollWidth')
        h, res = self.__ghost.evaluate('document.body.scrollHeight')
        self.__ghost.capture_to(dir + '\\%d_%d.png' % (i, j), region=(0, 0, w, h))

    def convert_action(self, action):
        r = urlparse.urlparse(self.location)
        host = slash(r.scheme + "://" + r.netloc)
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

    def test_form(self, form):
        print form
        if form.method == "post":
            print "post: pass"
            return
        for xss in self.xss_rsnake:
            postdata = ''
            for i in form.inputs:
                if i.name != '':
                    if i.type in ["", "text", "password"] or i.value == '':
                        postdata += '%s=%s&' % (i.name, xss)
                    elif i.type == 'hidden' and i.value != '':
                        postdata += '%s=%s&' % (i.name, i.value)  # hidden
            location = self.convert_action(form.action) + '?' + postdata
            print location
            try:
                self.__ghost.open(location)
            except TimeoutError:
                print "test: TimeoutError"
            self.__identify_xss()
        return

    def __str__(self):
        s = ""
        if len(self.__as) > 10:
            s += '<a>: %d\n' % len(self.__as)
        else:
            for a in self.__as:
                s += '%s\n' % a
        for input in self.__inputs:
            s += '%s\n' % input
        for button in self.__buttons:
            s += '%s\n' % button
        for textarea in self.__textareas:
            s += '%s\n' % textarea
        for form in self.__forms:
            s += '%s\n' % form
        return s[:-1] if s != "" else ""

    def exit(self):
        self.__ghost.hide()
        self.display('finish', '<b>$</b>')
        self.__ghost.sleep(60)
        self.__ghost.exit()


if __name__ == '__main__':
    '''
    import urllib2
    doc = urllib2.urlopen("http://esf.cd.fang.com/agenthome/").read()
    soup = BeautifulSoup(doc, from_encoding='gb18030')
    print soup.prettify()
    exit()
    '''
    for location in sites:
        start = time.clock()
        t = Test(location)
        t.go()
        end = time.clock()
        print 'time:', end - start
        break
