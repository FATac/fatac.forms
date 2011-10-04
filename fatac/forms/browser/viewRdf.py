from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request


class viewRdf(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/viewRdf.pt')

    def rdf(self):
        resp = request('http://stress:8080/ArtsCombinatoriesRest/getRdf')
        return resp.tee().read()
