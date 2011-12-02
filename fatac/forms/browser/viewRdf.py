from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca


class viewRdf(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/viewRdf.pt')

    def rdf(self):
        resp = request(self.retServidorRest() + '/getRdf')
        return resp.tee().read()
