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
from fatac.theme.browser.funcionsCerca import funcionsCerca

class updateExisting(BrowserView, funcionsCerca):
    
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/updateExisting.pt')
    
    def about(self):
        self.render2()
        oid = self.request.form['id']
        
        if type(self.className) == list:
            classList = ""
            for c in self.className: classList += c + ", "
            classList = classList[:-2]
        else:
            classList = self.className
        
        return str.replace(oid, "_", " ") + " (" + classList + ")"
    
    def objectId(self):
        oid = self.request.form['id']
        return oid
    
    def deleteLink(self):
        oid = self.request.form['id']
         
        return "deleteObject('" + oid + "')";
    
    def deleteConfirmedLink(self):
        oid = self.request.form['id']
        try:
            loc = self.request.form['locator']
        except KeyError:
            loc = ''
        return "deleteObjectConfirmed('" + oid + "','"+loc+"')";
    
    class resultItem:
        value = None
        link = None
        
        def __init__(self, value, link):
            self.value = value
            self.link = link
    
    def locator(self):
        try:
            oid = self.request.form['id']
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
            
            if pos is None:
                result.append(self.resultItem(oid,'javascript:goToObject("'+oid+'","'+str(idx)+'")'))
                
            return result
        except KeyError:
            oid = self.request.form['id']
            result = [self.resultItem(oid,'javascript:goToObject("'+oid+'","0")')]
            return result
    
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
        
        try:
            loc = self.request.form['locator']
        except KeyError:
            loc = ''

        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        if self.request.AUTHENTICATED_USER and self.request.AUTHENTICATED_USER.getId() is not None:
            usrId = '?u=' + self.request.AUTHENTICATED_USER.getId()
        else:
            usrId = ''

        resp = request(self.retServidorRest() + '/resource/' + oid + usrId)
        jsonResult = resp.tee().read()
        obj = json.loads(jsonResult)

        try:
            self.className = obj['rdf:type']
        except KeyError:
            self.className = ""
        
        if self.className != None:
            if type(self.className)==list:
                resp = request(self.retServidorRest() + '/classes/' + self.className[0] + '/form')
            else:
                resp = request(self.retServidorRest() + '/classes/' + self.className + '/form')
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
                    
            if self.request.get('pos', None):
                pos = self.request.form['pos']
                loclist = loc.split(",")[:int(pos)+1]
                loc2 = ''
                for l in loclist: loc2 += l + ","
                    
                controlList.append(myControls.HiddenInputControl('locator', loc2))
            else:
                controlList.append(myControls.HiddenInputControl('locator', loc + oid + ","))
            
            form = myControls.Form('updateObject', controlList)                
            self.html = form.render()
