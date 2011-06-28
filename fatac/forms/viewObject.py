import deform 
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from deform import Form
import ObjectInputWidget
from ObjectInputWidget import ObjectInputWidget

class viewObject(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    __call__ = ViewPageTemplateFile('templates/viewObject.pt')
        
    class resultItem:
        name = None
        value = None
        link = None
        
        def __init__(self, name, value, link):
            self.name = name
            self.value = value
            self.link = link
    
    def isAdmin(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)

        usrTyp = None
        if session.has_key('userType'):
            usrTyp = session['userType']
            
        if usrTyp == '4':
            return True
        else:
            return False
        
    def editLink(self):
        return "window.location='./updateExisting?id="+self.getOid()+"'";
    
    def mediaLink(self):
         return self.mLink
        
    def getOid(self):
        return self.request.form['id']

    def results(self):
        oid = self.getOid()
        resp = request('http://localhost:8080/ArtsCombinatoriesRest/getObject?id='+oid)
        jsonResult = resp.tee().read()
        obj = json.loads(jsonResult)

        try:
            className = obj['type']
        except KeyError:
            className = None
            
        hasFile = False
        resp = request('http://localhost:8080/ArtsCombinatoriesRest/getInsertObjectForm?className='+className)
        jsonResult = resp.tee().read()
        jsonTree = json.loads(jsonResult)
        
        result = list()
        self.mLink = None
        for s in jsonTree['inputList']:
            if s['controlType'] == 'fileInput':
                self.mLink = 'http://stress.upc.es:8080/ArtsCombinatoriesRest/getObjectFile?id='+oid
                
            try:
                currValue = obj[s['name']]
                if s['controlType'] == 'objectInput':
                    result.append(self.resultItem(s['name'], currValue, './viewObject?id='+currValue))
                else:
                    result.append(self.resultItem(s['name'], currValue, None))
            except KeyError:
                currValue = None

        return result
