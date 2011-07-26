from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request

class deleteObject(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    __call__ = ViewPageTemplateFile('templates/deleteObject.pt')

    def render(self):
        if 'delete' in self.request and 'objectId' in self.request:
            oid = self.request['objectId'];
            #resp = request('http://localhost:8080/ArtsCombinatoriesRest/objects/'+oid+'/delete')
            resp = request('http://localhost:8080/ArtsCombinatoriesRest/objects/'+oid+'/delete')
            
            result = resp.tee().read()
            if result == 'error':
                return 'Error'
            else:
                return result
        else:
            return 'Oops!'
