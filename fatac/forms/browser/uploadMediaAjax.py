import json
import urllib 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from zope.component import getUtility
from fatac.theme.browser.funcionsCerca import funcionsCerca

class uploadMediaAjax(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    def __call__(self):
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
                
                resp = request('http://localhost:8080/ArtsCombinatoriesRest/media/upload?fn='+urllib.quote_plus(upload.filename),
                                                method='POST',
                                                headers={'Content-Type': 'multipart/form-data'},
                                                body=upload)
                resp = resp.tee().read()
                self.urlValue = resp
                if resp != "error":            
                    return "<html><header><script>parent.mediaUrlPreview('"+resp+"'); </script></header><body></body></html>"
                else:
                    return "Error"
        
        return "Seleccioni un fitxer media"
    