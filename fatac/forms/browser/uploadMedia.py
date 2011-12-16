import json
import urllib 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from zope.component import getUtility
from fatac.theme.browser.funcionsCerca import funcionsCerca


class uploadMedia(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    __call__ = ViewPageTemplateFile('templates/uploadMedia.pt')
    
    def url(self):
        self.html = self.render2()
        try:
            if self.urlValue is not None:
                return self.urlValue
        except AttributeError:
            return ""
        
        return ""
    
    def render(self):
        return self.html
    
    def render2(self):
        if 'mediaurl' in self.request and self.request['mediaurl'] != '':
            self.urlValue = self.request['mediaurl']
        
        if 'mediafile' in self.request and self.request['mediafile'] != '':
            upload = self.request.get("mediafile")
            content = upload.read()
            parts = upload.filename.split(".")
            last = len(parts) - 1
            ext = parts[last]
            
            if content is not None and content != '':
                parts = upload.filename.split(".")
                last = len(parts) - 1
                ext = parts[last]
                
                resp = request('http://localhost:8080/ArtsCombinatoriesRest/media/upload?fn='+ext,
                                                method='POST',
                                                headers={'Content-Type': 'multipart/form-data'},
                                                body=upload)
                resp = resp.tee().read()
                self.urlValue = resp
                
                if resp != "error":            
                    return "<div><iframe width='600' height='400' src='"+resp+"'></iframe></div>\n"
                else:
                    return "Error"
            
        if 'f' in self.request:
            resp = self.request["f"]
            self.urlValue = resp
            return "<div><iframe width='600' height='400' src='"+resp+"'></iframe></div>\n"
        
        try:
            if self.urlValue is not None and self.urlValue!='':
                return "<div><iframe width='600' height='400' src='"+self.urlValue+"'></iframe></div>\n"
        except AttributeError:
            ""
            
        return "Seleccioni un fitxer media."
    