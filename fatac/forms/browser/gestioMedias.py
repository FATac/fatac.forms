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
    
    def getSearchText(self):
        if "search" in self.request.form:
            return self.request.form["search"]
        else:
            return "" 
    
    def getPag(self):
        if "pag" in self.request.form and self.request.form["pag"] != "":
            return self.request.form["pag"]
        else:
            return "0"
        
    def getPagPlus1(self):
        if "pag" in self.request.form and self.request.form["pag"] != "":
            pag = int(self.request.form["pag"])
        else:
            pag = 0
        
        return "$('#pagInput').val(" + str(pag + 1) + ");document.gestioMedias.submit();"
        
    def getPagMinus1(self):
        if "pag" in self.request.form and self.request.form["pag"] != "":
            pag = int(self.request.form["pag"])
            if pag < 1: return None
            return "$('#pagInput').val(" + str(pag - 1) + ");document.gestioMedias.submit();"
        else:
            return None
        
    
    def getMediaList(self):
        restUrl = self.retServidorRest()
        search = ""
        pag = ""
        if "action" in self.request.form:
            search = "?s="
            pag = "?pag="        
            action = self.request.form["action"]
            id = self.request.form["id"]
            if action == 'delete':
                request(restUrl + '/media/'+id+'/delete')
            if action == 'convert':
                request(restUrl + '/media/'+id+'/convert')
                
            if "search" in self.request.form:
                search = search + self.request.form["search"]
                pag = "&pag=";
            else:
                search = ""
                
            if "pag" in self.request.form:
                pag = pag + self.request.form["pag"]
            else:
                pag = ""
        
        resp = request(restUrl + '/media/list' + search + pag)
        jsonResult = resp.tee().read()
        jsonTree = json.loads(jsonResult)
        
        result = list()
        for it in jsonTree:
            itl = it.split(".")
            item = itl[0]
            format = ""
            if len(itl)>1: format = itl[1]
            result.append(self.myItem(restUrl + '/media/' + it, it, format))
        
        return result