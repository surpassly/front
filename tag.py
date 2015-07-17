# _*_coding:utf-8_*_


class Action:
    def __init__(self, path, params):
        self.path = path
        self.params = params


class Form:
    def __init__(self, action, id, method, name, outerHTML, as_, inputs, buttons):
        self.action = action
        self.id = id
        self.method = method
        self.name = name
        self.outerHTML = outerHTML
        self.as_ = as_
        self.inputs = inputs
        self.buttons = buttons

    def __str__(self):
        s = "<form action='%s' id='%s' method='%s' name='%s'>\n" % (self.action, self.id, self.method, self.name)
        s += '    <a>: %d\n' % len(self.as_)
        for input in self.inputs:
            s += '    ' + str(input) + '\n'
        for button in self.buttons:
            s += '    ' + button.outerHTML + '\n'
        s += "</form>"
        return s

class A:
    def __init__(self, href, outerHTML):
        self.href = href
        self.outerHTML = outerHTML.replace('\n', '')

    def __str__(self):
        return "<a' href='%s'>" % self.href

class Input:
    def __init__(self, id, name, type, value, outerHTML):
        self.id = id
        self.name = name
        self.type = type
        self.value = value
        self.outerHTML = outerHTML.replace('\n', '')
        
    def __str__(self):
        return "<input id='%s' name='%s' type='%s', value='%s'>" % (self.id, self.name, self.type, self.value)
    

class Button:
    def __init__(self, classname, id, name, type, outerHTML):
        self.classname = classname
        self.id = id
        self.name = name
        self.type = type
        self.outerHTML = outerHTML.replace('\n', '')
        
    def __str__(self):
        return "<button class = '%s' id='%s' name='%s' type='%s'>" % (self.classname, self.id, self.name, self.type)
