# _*_coding:utf-8_*_

import os, random, string
import urlparse, urllib2
from ghost import Ghost, TimeoutError
from bs4 import BeautifulSoup
from tag import *  # get_methods tags class
from sites import *

page_timeout = 30
alert_timeout = 3

tested_actions = []


def create_spy():
    count = random.choice(range(5, 10))
    return ''.join(random.choice(string.letters) for i in range(count))


def slash(url):
    if not url.endswith('/'):
        url += '/'
    return url


class Test():
    def __init__(self, ghost, location, mainwindow=None):
        self.ghost = ghost
        self.ghost.show()
        self.mainwindow = mainwindow
        self.hrefs = []
        self.inputs = []
        self.buttons = []
        self.textareas = []
        self.forms = []
        self.location = location
        self.spy = [create_spy(), create_spy()]
        self.xss_rsnake = xss_vectors  # fuzzdb.attack_payloads.xss.xss_rsnake

    def display(self, content, format=None, widget=None):
        print content
        if self.mainwindow:
            self.mainwindow.display(content, format, widget)

    def baidu_login(self):
        self.ghost.click("a[name=tj_login]")
        try:
            self.ghost.wait_for_selector("form[id=TANGRAM__PSP_8__form]")
            self.ghost.evaluate('''
                var form = document.querySelector('form[id=TANGRAM__PSP_8__form]');
                document.querySelector('input[id=TANGRAM__PSP_8__userName]').value = "surpassly";
                document.querySelector('input[id=TANGRAM__PSP_8__password]').value = "myself";
                document.querySelector('input[id=TANGRAM__PSP_8__submit]').click()
                ''', expect_loading=True)
            # self.__ghost.click("input[id=TANGRAM__PSP_8__submit]", expect_loading=True)
            self.ghost.sleep(10)
        except TimeoutError:
            pass

    def manual(self):
        xss = self.xss_rsnake[0].replace('"', '\\"')
        self.ghost.set_field_value('input[id=txtAddress]', '961289741@qq.com')
        self.ghost.evaluate('document.querySelector("input[id=txtAddress]").value = "%s"' % '961289741@qq.com')  #
        self.ghost.evaluate('document.querySelector("input[id=txtSubject]").value = "%s"' % xss)
        self.ghost.evaluate('document.querySelector("body[contenteditable=true]").innerHTML = "%s"' % xss)  #
        self.ghost.sleep(10)
        self.ghost.click('div[class="btn_r"]')
        self.ghost.evaluate('''
            var xss = "%s"
            var tagElements = document.querySelectorAll("textarea");
            for (var i = 0; i < tagElements.length; i++) {
                var text = tagElements[i];
                text.innerHTML = xss
            };
            tagElements = document.querySelectorAll("input");
            for (var i = 0; i < tagElements.length; i++) {
                var input = tagElements[i];
                if (input.type == "" || input.type == "text" || input.type == "password" || (input.type == "hidden" && input.value == "")) {
                    input.removeAttribute("onfocus");
                    input.removeAttribute("placeholder");
                    input.value = xss
                }
            };
            ''' % xss)

    def test(self):
        urllib2.urlopen('http://wedge.sinaapp.com/0')  # reset
        if self.mainwindow:
            self.mainwindow.console_split.clear()
            self.mainwindow.xss_split.clear()
        self.display("%s ...opening" % self.location, '<b>$</b>')
        times = 0
        while True:
            try:
                self.ghost.open(self.location)
                break
            except TimeoutError:
                times = times + 1
            if times == 5:
                self.display("TimeoutError", '<font color=red>$</font>')
        soup = BeautifulSoup(str(self.ghost.content), from_encoding='utf-8')
        self.__get_all_tags(soup)
        if str(self) != "":
            self.display(str(self))
            self.display('...testing', '<b>$</b>')
            self.display("%s ...testing" % self.location, '<b>$</b>', 'url')
            # self.manual()
            self.test_inputs()
            self.test_forms()  # regular
        else:
            self.display('get nothing', '<b>$</b>')

    def __get_all_tags(self, soup):
        self.hrefs = get_hrefs(soup)
        self.buttons = get_buttons(soup)
        self.inputs = get_inputs(soup)
        self.textareas = get_textareas(soup)
        # get_forms
        bs_forms = soup.find_all('form')
        for bs_form in bs_forms:
            attrs = get_attrs(["action", "id", "method", "name"], bs_form)
            for f in [get_hrefs(bs_form), get_buttons(bs_form), get_inputs(bs_form), get_textareas(bs_form)]:
                attrs.append(f)
            self.forms.append(Form(*attrs))
        # delete
        for form in self.forms:
            f_list = [form.hrefs, form.buttons, form.inputs, form.textareas]
            s_list = [self.hrefs, self.buttons, self.inputs, self.textareas]
            for i in range(0, len(f_list)):
                for f in f_list[i]:
                    for s in s_list[i]:
                        if f.outerHTML == s.outerHTML:
                            s_list[i].remove(s)
        return

    def test_inputs(self):
        for i, input in enumerate(self.inputs):
            if input.type in ['hidden', 'button', 'submit', 'reset']:  # interaction
                continue
            self.display(str(input))
            for tag in input.tags:
                self.display("    " + str(tag))
                flag = 0  # spy
                attr = ''
                value = ''
                if tag.id != '':
                    attr = 'id'
                    value = tag.id
                elif tag.class_ != '':
                    attr = 'class'
                    value = str(' '.join(tag.class_))
                for j, xss in enumerate(self.spy + self.xss_rsnake):
                    self.display(xss, widget='xss')
                    xss = xss.replace('"', '\\"')
                    try:
                        self.ghost.open(self.location)
                        self.ghost.evaluate('''
                        var xss = "%s"
                        var tagElements = document.querySelectorAll("textarea");
                        for (var i = 0; i < tagElements.length; i++) {
                            var text = tagElements[i];
                            text.innerHTML = xss
                        };
                        tagElements = document.querySelectorAll("input");
                        for (var i = 0; i < tagElements.length; i++) {
                            var input = tagElements[i];
                            if (input.type == "" || input.type == "text" || input.type == "password" || (input.type == "hidden" && input.value == "")) {
                                input.removeAttribute("onfocus");
                                input.removeAttribute("placeholder");
                                input.value = xss
                            }
                        };
                        ''' % xss)
                        self.ghost.click("%s[%s='%s']" % (tag.tag, attr, value), expect_loading=True)
                        if j < len(self.spy) and not self.__identify_spy(xss):
                            flag += 1
                            if flag == len(self.spy):
                                break
                        self.__identify_xss(j)
                        self.capture_page(i, j)
                    except TimeoutError:
                        self.display("test_inputs: TimeoutError", '<font color=red>$</font>', 'xss')
                        if j < len(self.spy):
                            flag += 1
                            if flag == len(self.spy):
                                break
                if flag == 0:
                    break

    def test_forms(self):
        for i, form in enumerate(self.forms):
            if form.action in tested_actions:  # duplicate
                continue
            else:
                tested_actions.append(form.action)
            self.display(str(form))
            flag = 0  # spy
            for j, xss in enumerate(self.spy + self.xss_rsnake):
                self.display(xss, widget='xss')
                xss = xss.replace('"', '\\"')
                try:
                    self.ghost.open(self.location)
                    self.ghost.evaluate('''
                    var xss = "%s"
                    var form = document.querySelectorAll("form")[%d];
                    var tagElements = form.querySelectorAll("textarea");
                    for (var i = 0; i < tagElements.length; i++) {
                        var text = tagElements[i];
                        text.innerHTML = xss
                    };
                    tagElements = form.querySelectorAll("input");
                    for (var i = 0; i < tagElements.length; i++) {
                        var input = tagElements[i];
                        if (input.type == "" || input.type == "text" || input.type == "password" || (input.type == "hidden" && input.value == "")) {
                            input.removeAttribute("onfocus");
                            input.removeAttribute("placeholder");
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
                    self.__identify_xss(j)
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
            result, resources = self.ghost.wait_for_text(spy, timeout=alert_timeout)
        except TimeoutError:
            pass
        '''
        finally:
            url, resources = self.__ghost.evaluate('window.location.href')
            self.display(str(url), "<a href='$'>$<a>", 'xss')
        '''
        return result

    def __identify_xss(self, i):
        flag = False
        try:
            result, resources = self.ghost.wait_for_alert(timeout=alert_timeout)
            self.display('alert: %s' % result, '<b>$</b>', 'xss')
            if result:
                flag = True  # identified
        except TimeoutError:
            pass
        try:  # SRC
            doc = urllib2.urlopen('http://wedge.sinaapp.com/r')
            result = BeautifulSoup(doc).find('body').string
            if result != '0' and result == '%d' % i:
                self.display('src: %s' % result, '<b>$</b>', 'xss')
        except TimeoutError:
            pass
        return flag

    def capture_page(self, i, j):
        r = urlparse.urlparse(self.location)
        dir = r.netloc + r.path.replace('/', '_')
        if not os.path.exists(os.getcwd() + '\\' + dir):
            os.mkdir(dir)
        w, res = self.ghost.evaluate('document.body.scrollWidth')
        h, res = self.ghost.evaluate('document.body.scrollHeight')
        if not w:
            w = 800
        if not h:
            h = 600
        self.ghost.capture_to(dir + '\\%d_%d.png' % (i, j), region=(0, 0, w, h))

    def __str__(self):
        s = ""
        if len(self.hrefs) > 10:
            s += '<a>: %d\n' % len(self.hrefs)
        else:
            for a in self.hrefs:
                s += '%s\n' % a
        for button in self.buttons:
            s += '%s\n' % button
        for input in self.inputs:
            s += '%s\n' % input
        for textarea in self.textareas:
            s += '%s\n' % textarea
        for form in self.forms:
            s += '%s\n' % form
        return s[:-1] if s != "" else ""


if __name__ == '__main__':
    reload(__import__('sys')).setdefaultencoding('utf-8')
    location = sites[0]
    ghost = Ghost().start()
    ghost._confirm_expected = True
    # ghost.load_cookies('513.txt')
    ghost.wait_timeout = page_timeout
    ghost.download_images = False
    t = Test(ghost, location)
    t.test()


