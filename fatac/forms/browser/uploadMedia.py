import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from fatac.theme.browser.interfaces import IFatacSettings


class uploadMedia(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    __call__ = ViewPageTemplateFile('templates/uploadMedia.pt')
    
    def getHost(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IFatacSettings)
        url = settings.rest_server
        return url
    
    def render(self):
        if 'mediafile' in self.request:
            upload = self.request.get("mediafile")
            
            resp = request('http://stress:8080/ArtsCombinatoriesRest/media/upload?fn=' + upload.filename,
                                            method='POST',
                                            headers={'Content-Type': 'multipart/form-data'},
                                            body=upload.read())
            resp = resp.tee().read()
            
            if resp != "error":            
                return "<div><iframe src='"+resp+"'></iframe></div>\n <div><a href='"+resp+"'>"+resp+"</a>&nbsp;<a href='"+resp+"'>Delete</a></div>"
            else:
                return "Error"
            
        if 'f' in self.request:
            resp = self.request["f"]
            return "<div><iframe src='"+resp+"'></iframe></div>\n <div><a href='"+resp+"'>"+resp+"</a></div>"
            
        return "Select a media to upload."
    