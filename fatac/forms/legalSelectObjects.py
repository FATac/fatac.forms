from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class legalSelectObjects(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
    
    __call__ = ViewPageTemplateFile('templates/legalSelectObjects.pt')
