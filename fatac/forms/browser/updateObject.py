import json
import myControls
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca

class updateObject(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/updateObject.pt')
    
    class resultItem:
        value = None
        link = None
        
        def __init__(self, value, link):
            self.value = value
            self.link = link
    
    def locator(self):
        try:
            oid = self.request.form['about']
            loc = self.request.form['locator']
            loclist = loc.split(",")[:-1]
            if self.request.get('pos', None):
                pos = self.request.form['pos']
                loclist = loclist[:int(pos)+1]
            else:
                pos = None
                        
            result = []
            idx = 0
            for l in loclist:
                result.append(self.resultItem(l,'javascript:goToObject("'+l+'","'+str(idx)+'")'))
                idx = idx + 1
                
            return result
        except KeyError:
            oid = self.request.form['id']
            result = [self.resultItem(oid,'javascript:goToObject("'+oid+'","0")')]
            return result
        
    def about(self):
        oid = self.request.form['about']        
        return str.replace(oid, "_", " ") + " (" + self.request['type'] + ")"

    def render(self):
        if 'submit' in self.request and 'type' in self.request:
            className = self.request['type']
            about = self.request['about']
            resp = request(self.retServidorRest() + '/classes/' + className + '/form')
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)

            jsonRequest = {'type': className}
            for s in jsonTree['inputList']:
                nameparts = s['name'].split(":")
                
                if len(nameparts)>1:
                    fieldName = nameparts[1]
                    prefix = nameparts[0]
                else:
                    fieldName = nameparts[0]
                    prefix = None
                
                if fieldName in self.request:
                    fieldValue = self.request[fieldName]
                    if fieldName+'_lang' in self.request:
                        tmp = []
                        fieldLang = self.request[fieldName+'_lang']
                        if type(fieldValue) == list:
                            for v,l in zip(fieldValue, fieldLang):
                                if fieldLang!='':
                                    tmp.append(v+'@'+l)
                                else:
                                    tmp.append(v)
                        else:
                            if fieldLang!='':
                                tmp = fieldValue+'@'+fieldLang
                            else:
                                tmp = fieldValue
                        
                        if tmp == '@': tmp = ''    
                        fieldValue = tmp
                            
                    if fieldName+'_prefix' in self.request:
                        fieldPrefix = self.request[fieldName+'_prefix']
                        if type(fieldPrefix) == list:
                            fieldName = fieldPrefix[0] + ":" + fieldName
                        else:
                            fieldName = fieldPrefix + ":" + fieldName
                    
                    jsonRequest[fieldName] = fieldValue

            resp = request(self.retServidorRest() + '/resource/'+about+'/update',
                                method='POST',
                                headers={'Content-Type': 'application/json'},
                                body=json.dumps(jsonRequest))

            result = resp.tee().read()
            
            try:
                myformHtml = "<form name='myform'><input type='hidden' name='locator' value='"+self.request.form['locator']+"'></form> <div id='mydiv'></div>"
            except KeyError:
                myformHtml = "" 
            
            if result == 'success':
                return "Objecte desat <a href='./genericView?idobjecte=" + self.request.form['about'] + "' target='_fitxaWindow'>Veure fitxa</a>" + myformHtml 
            else:
                return "Hi ha hagut algun error."
        else:
            return 'Oops!'
