# _*_coding:utf-8_*_

class Action:
    def __init__(self, path, params):
        self.path = path
        self.params = params

class Form:
    def __init__(self, action, id, method, name, inputs):
        self.action = action
        self.id = id
        self.method = method
        self.name = name
        self.inputs = inputs
    
    def __str__(self):
        s = "<form action='%s' id='%s' method='%s' name='%s'>\n" % (self.action, self.id, self.method, self.name)
        for input, input in enumerate(self.inputs):
            s += '\t' + str(input) + '\n'
        s += "</form>"
        return s


class Input:
    def __init__(self, id, name, type, value):
        self.id = id
        self.name = name
        self.type = type
        self.value = value
        
    def __str__(self):
        return "<input id='%s' name='%s' type='%s', value='%s'>" % (self.id, self.name, self.type, self.value)