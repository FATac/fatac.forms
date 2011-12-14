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
    
    def render(self):
        if 'mediafile' in self.request:
            upload = self.request.get("mediafile")
            
            parts = upload.filename.split(".")
            last = len(parts) - 1
            ext = parts[last]
            
            resp = request('http://localhost:8080/ArtsCombinatoriesRest/media/upload?fn='+ext,
                                            method='POST',
                                            headers={'Content-Type': 'multipart/form-data'},
                                            body=upload.read())
            resp = resp.tee().read()
            
            if resp != "error":            
                return "<div><iframe src='"+resp+"'></iframe></div>\n <div><a href='"+resp+"'>"+resp+"</a>&nbsp;<a href='"+resp+"/delete'>Delete</a></div>"
            else:
                return "Error"
            
        if 'f' in self.request:
            resp = self.request["f"]
            return "<div><iframe src='"+resp+"'></iframe></div>\n <div><a href='"+resp+"'>"+resp+"</a></div>&nbsp;<a href='"+resp+"/delete'>Delete</a></div>"
            
        return "Select a media to upload."
    