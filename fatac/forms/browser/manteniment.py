import json
import urllib
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca

class manteniment(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/manteniment.pt')
    
    def action(self):
        result = "Selecciona una tasca a realitzar"
        if 'action' in self.request.form:
            action = self.request.form['action']
            if action == 'reset':                
                if 'confirmReset' in self.request.form:
                    confirmReset = self.request.form['confirmReset']
                    if confirmReset != '':
                        call = self.retServidorRest() + '/reset?confirm=' + urllib.quote_plus(confirmReset)
                        resp = request(call)
                        result = resp.tee().read()
                        result = "Reset: " + result
                    else:
                        result = "Reset: Falta confirmar"
                else:
                    resp = "Reset: Falta confirmar"
            if action == 'ontology':
                resp = request(self.retServidorRest() + '/reset?option=ontology')
                result = resp.tee().read()
                result = 'Ontologies: ' + result
            if action == 'oai':
                resp = request(self.retServidorRest() + '/oai')
                result = resp.tee().read()
                result = 'OAI: ' + result
            if action == 'index':
                resp = request(self.retServidorRest() + '/solr/reload')
                result = resp.tee().read()
                result = 'Indexar: ' + result
        
        return result
                