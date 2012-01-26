import json
import urllib
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca

class gestioMedias(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/gestioMedias.pt')
    
    class myItem:
        def __init__(self, itemUrl, itemId, format):
            self.url = itemUrl
            self.id =  itemId
            self.format = format
            self.urlDelete = "javascript:call('delete','"+itemId+"');"
            self.urlConvert = "javascript:call('convert','"+itemId+"');"
    
    def getMediaList(self):
        restUrl = self.retServidorRest()
        if "action" in self.request.form:
            action = self.request.form["action"]
            id = self.request.form["id"]
            if action == 'delete':
                request(restUrl + '/media/'+id+'/delete')
            if action == 'convert':
                request(restUrl + '/media/'+id+'/convert')
        
        
        resp = request(restUrl + '/media/list')
        jsonResult = resp.tee().read()
        jsonTree = json.loads(jsonResult)
        
        result = list()
        for it in jsonTree:
            itl = it.split(".")
            item = itl[0]
            format = ""
            if len(itl)>1: format = itl[1]
            result.append(self.myItem(restUrl + '/media/' + item, item, format))
        
        return result