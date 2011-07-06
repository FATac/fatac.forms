import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
import ObjectInputWidget
from ObjectInputWidget import ObjectInputWidget

class legalDataAjax(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    def __call__(self):
        keyName = self.request['keyName']
        keyValue = self.request['keyValue']
        userId = self.request['userId']
        
        resp = request('http://localhost:8080/ArtsCombinatoriesRest/legalRestoreData?key='+keyName+'&value='+keyValue+'&userId='+userId)
        jsonResult = resp.tee().read()
        
        if jsonResult == 'error':
            return ""

        jsonTree = json.loads(jsonResult)
        
        result = '<script>'
        for s in jsonTree:
            val = ''
            if s.has_key('defaultValue'): val = s['defaultValue'];
            result = result + 'setFormValue("' + s['name'] + '","' + val + '"); ';
            
        result = result + ' </script>'
        return result