# _*_coding:utf-8_*_


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


def get_buttons(soup):
    res = []
    bs_buttons = soup.find_all('button')
    for bs_button in bs_buttons:
        attrs = get_attrs(["class", "id", "name", "type"], bs_button)
        res.append(Button(*attrs))
    return res


def get_inputs(soup):
    res = []
    bs_inputs = soup.find_all('input')
    for bs_input in bs_inputs:
        attrs = get_attrs(["class", "id", "name", "type", "value"], bs_input)
        tags = []
        if attrs[3] not in ['hidden', 'button', 'submit', 'reset']:  # type
            bs_parent = bs_input.parent
            while True:
                if not bs_parent:
                    break
                for child in bs_parent:
                    try:
                        if str(child).strip() != "":
                            tag_attrs = [child.name]
                            tag_attrs += get_attrs(["class", "id", "name", "type"], child)
                            if tag_attrs[-1] != attrs[-1]:  # outerHTML
                                if (tag_attrs[1] == '' and tag_attrs[2] == ''):  # id name
                                    continue
                                if tag_attrs[0] == 'input' and tag_attrs[4] not in ['button', 'submit', 'reset']:
                                    continue
                                tags.append(Tag(*tag_attrs))
                    except AttributeError:  # no attribute 'attrs'
                        pass
                l = len(tags)
                if l == 0:
                    tags = []
                    bs_parent = bs_parent.parent
                else:
                    break
        attrs.append(tags)
        res.append(Input(*attrs))
    return res


def get_tags(soup):
    res = []
    for child in soup:
        if str(child).strip() != "":
            attrs = [child.name]
            attrs += get_attrs(["class", "id", "name", "type"], child)
            res.append(Tag(*attrs))
    return res


def get_textareas(soup):
    res = []
    bs_textareas = soup.find_all('textarea')
    for bs_textarea in bs_textareas:
        attrs = get_attrs(["class", "id", "name", "value"], bs_textarea)
        res.append(TextArea(*attrs))
    return res


class Form:
    def __init__(self, action, id, method, name, outerHTML, as_, buttons, inputs, textareas):
        self.action = action
        self.id = id
        self.method = method
        self.name = name
        self.outerHTML = outerHTML
        self.as_ = as_
        self.buttons = buttons
        self.inputs = inputs
        self.textareas = textareas

    def __str__(self):
        s = "<form action='%s' id='%s' method='%s' name='%s'>\n" % (self.action, self.id, self.method, self.name)
        if len(self.as_) > 10:
            s += '    <a>: %d\n' % len(self.as_)
        else:
            for a in self.as_:
                s += '    %s\n' % a
        for button in self.buttons:
            s += '    %s\n' % button
        for input in self.inputs:
            s += '    %s\n' % input
        for textarea in self.textareas:
            s += '    %s\n' % textarea
        s += "</form>"
        return s


class A:
    def __init__(self, class_, href, outerHTML):
        self.class_ = class_
        self.href = href
        self.outerHTML = outerHTML.replace('\n', '')

    def __str__(self):
        return "<a class='%s' href='%s'>" % (self.class_, self.href)


class Button:
    def __init__(self, class_, id, name, type, outerHTML):
        self.class_ = class_
        self.id = id
        self.name = name
        self.type = type
        self.outerHTML = outerHTML.replace('\n', '')

    def __str__(self):
        return "<button class = '%s' id='%s' name='%s' type='%s'>" % (self.class_, self.id, self.name, self.type)


class Input:
    def __init__(self, class_, id, name, type, value, outerHTML, tags = None):
        self.class_ = class_
        self.id = id
        self.name = name
        self.type = type
        self.value = value
        self.outerHTML = outerHTML.replace('\n', '')
        self.tags = tags

    def __str__(self):
        return "<input class= '%s' id='%s' name='%s' type='%s', value='%s'>" % (self.class_, self.id, self.name, self.type, self.value)


class Tag:
    def __init__(self, tag, class_, id, name, type, outerHTML):
        self.tag = tag
        self.class_ = class_
        self.id = id
        self.name = name
        self.type = type
        self.outerHTML = outerHTML.replace('\n', '')

    def __str__(self):
        return "<%s class = '%s' id='%s' name='%s' type='%s'>" % (self.tag, self.class_, self.id, self.name, self.type)


class TextArea:
    def __init__(self, class_, id, name, value, outerHTML):
        self.class_ = class_
        self.id = id
        self.name = name
        self.value = value
        self.outerHTML = outerHTML.replace('\n', '')

    def __str__(self):
        return "<textarea class = '%s' id='%s' name='%s' value='%s'>" % (self.class_, self.id, self.name, self.value)
