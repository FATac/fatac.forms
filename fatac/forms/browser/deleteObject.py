from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca


class deleteObject(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/deleteObject.pt')


    def render(self):
        if 'objectId' in self.request:
            oid = self.request['objectId']
            resp = request(self.retServidorRest() + '/resource/' + oid + '/delete', method='DELETE')

            result = resp.tee().read()
            return result + "<br/><br/><a href='./inici'>Inici</>"
        else:
            return 'Oops!'
