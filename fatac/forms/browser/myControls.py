class Form(object):
    def __init__(self, action, controlList, method='post'):
        self.action = action
        self.controlList = controlList
        self.method = method
        
    def render(self):
        js = "  "
        
        html = "<form action='"+self.action+"' method='"+self.method+"' name='myform'>\n"
        for control in self.controlList:
            html += control.render()
        
        html += "<input name='submit' type='submit' value='Desar' >\n"
        html += "</form>\n"
        html += "<div id='mydiv'></div>\n"
        
        return html

class GenericControl(object):
    def __init__(self, label, name, value, lang='', required=False, multi=True):
        self.label = label
        self.value = value
        self.lang = lang
        self.required = required
        self.multi = multi
        
        nameparts = name.split(":")
        if len(nameparts)>1:
            self.prefix = nameparts[0]
            self.name = nameparts[1]
        else:
            self.prefix = None        
            self.name = name

class TextControl(GenericControl):    
    def render(self):
        html = "<div id='"+self.name.replace(u".",u"")+"_cntrl'>\n"
        valueList = []
        if type(self.value) == list:
            valueList = self.value
        else:
            valueList = [self.value]
            
        if self.lang is not None:
            if type(self.lang) == list:
                langList = self.lang
            else:
                langList = [self.lang]
        else:
            langList = []
            
        for idxi, v in enumerate(map(None, valueList, langList)):
            idx = str(idxi)
            html += "    <div id='"+self.name+"_"+idx+"' >\n"
            if self.multi and self.multi == True:
                html += "        <a onclick='addControl(\""+self.name.replace(u".",u"")+"\")'>+</a>&nbsp;<a onclick='removeControl(\""+self.name.replace(u".",u"")+"\",this)'>-</a>&nbsp;\n"
            html += "        <label>\n"+self.label+"</label>\n"
            html += "        <input type='text' name='"+self.name+"' value='"+v[0]+"'>\n"
            if v[1] is not None:
                html += "        &nbsp;<input type='text' name='"+self.name+"_lang' onchange='autocompleteLanguages(this);' value='"+v[1]+"' size='2'>\n"
            if self.prefix is not None:
                html += "        <input type='hidden' name='"+self.name+"_prefix' value='"+self.prefix+"'>\n"
            html += "    </div>\n"
            
        html += "</div>\n"
        
        return html
    
class DateControl(GenericControl):    
    def render(self):
        html = "<div id='"+self.name.replace(u".",u"")+"_cntrl'>\n"
        valueList = []
        if type(self.value) == list:
            valueList = self.value
        else:
            valueList = [self.value]
        
        for idxi, v in enumerate(valueList):
            idx = str(idxi)
            html += "    <div id='"+self.name+"_"+idx+"' >\n"
            html += "        <a onclick='addControl(\""+self.name.replace(u".",u"")+"\")'>+</a>&nbsp;<a onclick='removeControl(\""+self.name.replace(u".",u"")+"\",this)'>-</a>&nbsp;<label>\n"+self.label+"</label>\n"
            html += "        <input type='date' name='"+self.name+"' value='"+v+"' size='9'>\n"
            if self.prefix is not None:
                html += "        <input type='hidden' name='"+self.name+"_prefix' value='"+self.prefix+"'>\n"
            html += "    </div>\n"
            
        html += "</div>\n"
        
        return html
    
class NumberControl(GenericControl):    
    def render(self):
        html = "<div id='"+self.name.replace(u".",u"")+"_cntrl'>\n"
        valueList = []
        if type(self.value) == list:
            valueList = self.value
        else:
            valueList = [self.value]
        
        for idxi, v in enumerate(valueList):
            idx = str(idxi)
            html += "    <div id='"+self.name+"_"+idx+"' >\n"
            html += "        <a onclick='addControl(\""+self.name.replace(u".",u"")+"\")'>+</a>&nbsp;<a onclick='removeControl(\""+self.name.replace(u".",u"")+"\",this)'>-</a>&nbsp;<label>\n"+self.label+"</label>\n"
            html += "        <input type='text' name='"+self.name+"' value='"+v+"' size='9' onkeypress='validateNumber(event)' >\n"
            if self.prefix is not None:
                html += "        <input type='hidden' name='"+self.name+"_prefix' value='"+self.prefix+"'>\n"
            html += "    </div>\n"
            
        html += "</div>\n"
        
        return html
        
class TextAreaControl(GenericControl):
    def render(self):
        html = "<div id='"+self.name.replace(u".",u"")+"_cntrl'>\n"
        valueList = []
        if type(self.value) == list:
            valueList = self.value
        else:
            valueList = [self.value]

        if self.lang is not None:
            if type(self.lang) == list:
                langList = self.lang
            else:
                langList = [self.lang]
        else:
            langList = []
            
        for idxi, v in enumerate(map(None, valueList, langList)):
            idx = str(idxi)
            html += "    <div id='"+self.name+"_"+idx+"' >\n"
            html += "        <a onclick='addControl(\""+self.name.replace(u".",u"")+"\")'>+</a>&nbsp;<a onclick='removeControl(\""+self.name.replace(u".",u"")+"\",this)'>-</a>&nbsp;<label>\n"+self.label+"</label>\n"
            html += "        <textarea class='expand' rows=1 type='text' name='"+self.name+"'>\n"+v[0]+"</textarea>\n"
            if v[1] is not None:
                html += "        <input type='text' name='"+self.name+"_lang' onchange='autocompleteLanguages(this);' value='"+v[1]+"' size='2'>\n"
            if self.prefix is not None:
                html += "        <input type='hidden' name='"+self.name+"_prefix' value='"+self.prefix+"'>\n"
            html += "    </div>\n"
            
        html += "</div>\n"
        
        return html
    
class ObjectInputControl(GenericControl):
    def __init__(self, label, name, value, classNames):
        self.label = label
        self.value = value
        self.classNames = classNames
        
        nameparts = name.split(":")
        if len(nameparts)>1:
            self.prefix = nameparts[0]
            self.name = nameparts[1]
        else:
            self.prefix = None        
            self.name = name    
    
    def render(self):
        html = "<div id='"+self.name.replace(u".",u"")+"_cntrl'>\n"
        valueList = []
        if type(self.value) == list:
            valueList = self.value
        else:
            valueList = [self.value]
        
        for idxi, v in enumerate(valueList):
            idx = str(idxi)
            html += "    <div id='"+self.name+"_"+idx+"' >\n"
            html += "        <a onclick='addControl(\""+self.name.replace(u".",u"")+"\")'>+</a>&nbsp;<a onclick='removeControl(\""+self.name.replace(u".",u"")+"\",this)'>-</a>&nbsp;<label>\n"+self.label+"</label>\n"
            html += "        <input type='text' name='"+self.name+"' value='"+v+"' class='objectinput'>&nbsp;<input type='image' src='++resource++fatac.forms.images/crear.png' title='Crear' onclick='createObject(this, \""+self.classNames+"\"); return false;' >&nbsp;<input type='image' src='++resource++fatac.forms.images/cercar.png' title='Cercar' onclick='seekObject(this, \""+self.classNames+"\"); return false;' >\n"
            html += "        <input type='image' src='++resource++fatac.forms.images/anar.png' onclick='goToObject(getObjectInputValue(this)); return false;' title='Anar-hi'>\n"
            if self.prefix is not None:
                html += "        <input type='hidden' name='"+self.name+"_prefix' value='"+self.prefix+"'>\n"
            html += "    </div>\n"
            
        html += "</div>\n"
        
        return html

class HiddenInputControl(GenericControl):
    def __init__(self, name, value, required=False):
        self.value = value
        self.required = required
        
        nameparts = name.split(":")
        if len(nameparts)>1:
            self.prefix = nameparts[0]
            self.name = nameparts[1]
        else:
            self.prefix = None        
            self.name = name
    
    def render(self):
        return "    <input type='hidden' name='"+self.name+"' value='"+self.value+"'>\n"
    
class CheckControl(GenericControl):    
    def __init__(self, label, name, value):
        self.label = label
        self.value = value
        
        nameparts = name.split(":")
        if len(nameparts)>1:
            self.prefix = nameparts[0]
            self.name = nameparts[1]
        else:
            self.prefix = None        
            self.name = name
        
    def render(self):
        chcked = ''
        if self.value and self.value == True: chcked = 'checked'
        
        html = "<div id='"+self.name.replace(u".",u"")+"_cntrl'>\n"
        html += "    <div id='"+self.name+"' >\n"
        html += "        <label>\n"+self.label+"</label>\n"
        html += "        <input type='checkbox' name='"+self.name+"' "+chcked+">\n"
        if self.prefix is not None:
            html += "        <input type='hidden' name='"+self.name+"_prefix' value='"+self.prefix+"'>\n"
        html += "    </div>\n"
        html += "</div>\n"
        
        return html
    
class FileUrlInput(GenericControl):
    def render(self):
        html = "<div id='"+self.name.replace(u".",u"")+"_cntrl'>\n"
        valueList = []
        if type(self.value) == list:
            valueList = self.value
        else:
            valueList = [self.value]

        for idxi, v in enumerate(valueList):
            idx = str(idxi)
            html += "    <div id='"+self.name+"_"+idx+"' >\n"
            html += "        <a onclick='addControl(\""+self.name.replace(u".",u"")+"\")'>+</a>&nbsp;<a onclick='removeControl(\""+self.name.replace(u".",u"")+"\",this)'>-</a>&nbsp;<label>\n"+self.label+"</label>\n"
            html += "        <input type='text' name='"+self.name+"' value='"+v+"' onclick='showMediaSelector(this)'>\n"
            if self.prefix is not None:
                html += "        <input type='hidden' name='"+self.name+"_prefix' value='"+self.prefix+"'>\n"
            html += "    </div>\n"
            
        html += "</div>\n"
        
        return html

    
        