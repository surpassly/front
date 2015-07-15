# _*_coding:utf-8_*_


class Action:
    def __init__(self, path, params):
        self.path = path
        self.params = params


class Form:
    def __init__(self, action, id, method, name, inputs, buttons, outerHTML):
        self.action = action
        self.id = id
        self.method = method
        self.name = name
        self.inputs = inputs
        self.buttons = buttons
        self.outerHTML = outerHTML

    def __str__(self):
        s = "<form action='%s' id='%s' method='%s' name='%s'>\n" % (self.action, self.id, self.method, self.name)
        for input in self.inputs:
            s += '\t' + str(input) + '\n'
        for button in self.buttons:
            s += '\t' + str(button) + '\n'
        s += "</form>"
        return s


class Input:
    def __init__(self, id, name, type, value, outerHTML):
        self.id = id
        self.name = name
        self.type = type
        self.value = value
        self.outerHTML = outerHTML
        
    def __str__(self):
        return "<input id='%s' name='%s' type='%s', value='%s'>" % (self.id, self.name, self.type, self.value)
    

class Button:
    def __init__(self, classname, id, name, type, outerHTML):
        self.classname = classname
        self.id = id
        self.name = name
        self.type = type
        self.outerHTML = outerHTML
        
    def __str__(self):
        return "<button class = '%s' id='%s' name='%s' type='%s'>" % (self.classname, self.id, self.name, self.type)
