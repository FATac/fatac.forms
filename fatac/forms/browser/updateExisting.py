import deform
import colander
import json
import myControls
import re
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from widgets import ObjectInputWidget
from fatac.forms import FatAcMessageFactory as _

class updateExisting(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/updateExisting.pt')
    
    def about(self):
        self.render2()
        oid = self.request.form['id']
        
        if type(self.className) == list:
            classList = ""
            for c in self.className: classList += c + " - "
            classList = classList[:-2]
        else:
            classList = self.className
        
        return str.replace(oid, "_", " ") + " ( " + classList + ")"
    
    def separate(self, value):
        if type(value) != list:
            if value is None or value == '': 
                return ['', '']
            
            res = re.findall('@[a-z]{2}$', value)
            if res == []:
                return [value, '']
            else:
                return [value[:-3], res[0][1:]]
        else:
            result = []
            for v in value: result.append(self.separate(v))
            return result

    def render(self):
        return self.html
    
    def render2(self):
        oid = self.request.form['id']

        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        if self.request.AUTHENTICATED_USER and self.request.AUTHENTICATED_USER.getId() is not None:
            usrId = '?u=' + self.request.AUTHENTICATED_USER.getId()
        else:
            usrId = ''

        resp = request('http://stress:8080/ArtsCombinatoriesRest/resource/' + oid + usrId)
        jsonResult = resp.tee().read()
        obj = json.loads(jsonResult)

        try:
            self.className = obj['rdf:type']
        except KeyError:
            self.className = None
        
        if self.className != None:
            resp = request('http://stress:8080/ArtsCombinatoriesRest/classes/' + self.className[0] + '/form')
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)
            
            controlList = []
            controlList.append(myControls.HiddenInputControl('type', jsonTree['className']))
            controlList.append(myControls.HiddenInputControl('about', oid))
            
            for s in jsonTree['inputList']:
                try:
                    currValue = obj[s['name']]
                except KeyError:
                    currValue = ''
            
                valueType = type(currValue)
                if valueType != list: currValue = [currValue]
                
                if s['controlType'] == 'textInput':
                    sep = zip(*self.separate(currValue)) 
                    controlList.append(myControls.TextControl(_(s['name']), s['name'], list(sep[0]), list(sep[1])))
                elif s['controlType'] == 'textAreaInput':
                    sep = zip(*self.separate(currValue)) 
                    controlList.append(myControls.TextAreaControl(_(s['name']), s['name'], list(sep[0]), list(sep[1])))
                elif s['controlType'] == 'dateInput':
                    controlList.append(myControls.DateControl(_(s['name']), s['name'], currValue))
                elif s['controlType'] == 'objectInput':
                    controlList.append(myControls.ObjectInputControl(_(s['name']), s['name'], currValue, s['objectClass']))
                elif s['controlType'] == 'checkInput':
                    if currValue == 'true':
                        controlList.append(myControls.CheckControl(_(s['name']), s['name'], True))
                    else:
                        controlList.append(myControls.CheckControl(_(s['name']), s['name'], False))
                elif s['controlType'] == 'fileInput':
                    controlList.append(myControls.FileUrlInput( _(s['name']), s['name'], currValue))
            
            form = myControls.Form('updateObject', controlList)                
            self.html = form.render()
