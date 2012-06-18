import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca


class uploadObject(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/uploadObject.pt')

    def render(self):
        if 'submit' in self.request and 'type' in self.request:
            className = self.request['type']
            about = self.request['about']
            resp = request(self.retServidorRest() + '/classes/' + className + '/form')
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)

            jsonRequest = {'type': className, 'about':about}
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
                                if l!='': tmp.append(v+'@'+l)
                                else: tmp.append(v)
                        else:
                            if fieldLang!='': tmp = fieldValue+'@'+fieldLang
                            else: tmp = fieldValue
                        
                        if tmp == '@': tmp = ''    
                        fieldValue = tmp
                            
                    if fieldName+'_prefix' in self.request:
                        fieldPrefix = self.request[fieldName+'_prefix']
                        if type(fieldPrefix) == list:
                            fieldName = fieldPrefix[0] + ":" + fieldName
                        else:
                            fieldName = fieldPrefix + ":" + fieldName
                    
                    jsonRequest[fieldName] = fieldValue

            resp = request(self.retServidorRest() + '/resource/upload',
                                method='PUT',
                                headers={'Content-Type': 'application/json'},
                                body=json.dumps(jsonRequest))

            result = resp.tee().read()

	    self.newId = result
            
            if result!='error':
                if '__relatedObject' in self.request:
                    return "&nbsp;<a href='javascript:opener.setCurrentInputValue(\""+result+"\"); opener.focus(); window.close();'>[Seleccionar]</a>"
                else:
                    return "<a href='./genericView?idobjecte="+result+"' target='_fitaWindow'>Veure fitxa</a>"
        else:
            return 'Oops!'
