# _*_coding:utf-8_*_


class Form:
    def __init__(self, action, id, method, name, outerHTML, as_, inputs, buttons, textareas):
        self.action = action
        self.id = id
        self.method = method
        self.name = name
        self.outerHTML = outerHTML
        self.as_ = as_
        self.inputs = inputs
        self.buttons = buttons
        self.textareas = textareas

    def __str__(self):
        s = "<form action='%s' id='%s' method='%s' name='%s'>\n" % (self.action, self.id, self.method, self.name)
        if len(self.as_) > 10:
            s += '    <a>: %d\n' % len(self.as_)
        else:
            for a in self.as_:
                s += '   %s\n' % a
        for input in self.inputs:
            s += '   %s\n' % input
        for button in self.buttons:
            s += '   %s\n' % button
        for textarea in self.textareas:
            s += '   %s\n' % textarea
        s += "</form>"
        return s


class A:
    def __init__(self, class_, href, outerHTML):
        self.class_ = class_
        self.href = href
        self.outerHTML = outerHTML.replace('\n', '')

    def __str__(self):
        return "<a class='%s' href='%s'>" % (self.class_, self.href)


class Input:
    def __init__(self, class_, id, name, type, value, outerHTML):
        self.class_ = class_
        self.id = id
        self.name = name
        self.type = type
        self.value = value
        self.outerHTML = outerHTML.replace('\n', '')
        
    def __str__(self):
        return "<input class= '%s'id='%s' name='%s' type='%s', value='%s'>" % (self.class_, self.id, self.name, self.type, self.value)


class TextArea:
    def __init__(self, class_, id, name, value, outerHTML):
        self.class_ = class_
        self.id = id
        self.name = name
        self.value = value
        self.outerHTML = outerHTML.replace('\n', '')

    def __str__(self):
        return "<textarea class = '%s' id='%s' name='%s' value='%s'>" % (self.class_, self.id, self.name, self.value)


class Button:
    def __init__(self, class_, id, name, type, outerHTML):
        self.class_ = class_
        self.id = id
        self.name = name
        self.type = type
        self.outerHTML = outerHTML.replace('\n', '')
        
    def __str__(self):
        return "<button class = '%s' id='%s' name='%s' type='%s'>" % (self.class_, self.id, self.name, self.type)


class Tag:
    def __init__(self, tag, class_, id, name, outerHTML):
        self.tag = tag
        self.class_ = class_
        self.id = id
        self.name = name
        self.outerHTML = outerHTML.replace('\n', '')

    def __str__(self):
        return "<%s class = '%s' id='%s' name='%s'>" % (self.tag, self.class_, self.id, self.name)
